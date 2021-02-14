import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import skimage.io
import streamlit as st
from skimage import data, exposure
from skimage.color import label2rgb
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.segmentation import clear_border

EXAMPLES = [""] + [name for name in data.__all__ if name not in ["data_dir", "download_all"]]


def read_image(input_file):
    image_data = skimage.io.imread(input_file)
    return image_data


def st_imshow(image):
    fig, ax = plt.subplots()
    ax.imshow(image)
    st.write(fig)


def plot_labeled_image(image, label_image, regions, plot_overlay=True, min_region_area=100):
    """Plot image and the detected object labels

    Arguments:
        image: original image as numpy ndarray
        label_image: label image data array
        regions: detected regions (bounding boxes)
        plot_overlay: colorize detected labels areas
        min_region_area: minimum region area to show
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    if plot_overlay:
        # to make the background transparent, pass the value of `bg_label`,
        # and leave `bg_color` as `None` and `kind` as `overlay`
        image_label_overlay = label2rgb(label_image, image=image, bg_label=0)
        ax.imshow(image_label_overlay)
    else:
        ax.imshow(image)

    for region in regions:
        # take regions with large enough areas
        if region.area >= min_region_area:
            # draw rectangle around segmented coins
            minr, minc, maxr, maxc = region.bbox
            rect = mpatches.Rectangle(
                (minc, minr), maxc - minc, maxr - minr, fill=False, edgecolor="red", linewidth=2
            )
            ax.add_patch(rect)

    ax.set_axis_off()
    plt.tight_layout()
    return fig


def main():
    """The main Streamlit application
    """
    st.sidebar.subheader("Select example or upload file")
    example = st.sidebar.selectbox("Example", EXAMPLES)
    input_file = st.sidebar.file_uploader("Image file")

    if input_file:
        original_image_data = read_image(input_file)
    elif example:
        original_image_data = getattr(data, example)()
    else:
        st.warning("Select or upload image first")
        return

    st.sidebar.subheader("Gamma adjust")
    gamma = st.sidebar.slider("Gamma", 0.0, 10.0, 1.0)
    gain = st.sidebar.slider("Gain", 0.0, 10.0, 1.0)

    image_data = exposure.adjust_gamma(original_image_data, gamma, gain)
    image = np.atleast_3d(image_data)[:, :, 0]

    col1, col2 = st.beta_columns(2)
    with col1:
        st.write("Original image")
        st_imshow(original_image_data)
    with col2:
        st.write("Gamma-corrected image")
        st_imshow(image_data)

    st.sidebar.subheader("Labeling parameters")
    closing_threshold = st.sidebar.slider("Closing threshold", 0, 200, 100, step=10)
    square_size = st.sidebar.slider("Square size", 0, 20, 5, step=1)
    binary_image = closing(image > closing_threshold, square(square_size))

    st_imshow(binary_image)

    # remove artifacts connected to image border
    cleared = clear_border(binary_image)
    # label image regions
    label_image = label(cleared)
    # Ex: add minimum region area parameter via slider
    regions = regionprops(label_image)

    st.subheader("Detected regions")
    st.write(f"Found {len(regions)} regions.")
    # EXERCISE 1: add a checkbox input for controlling the plot_overlay parameter of plot_labeled_image
    # EXERCISE 2: add a slider or number_input to control the min_region_area parameter
    fig = plot_labeled_image(image, label_image, regions)
    st.write(fig)


if __name__ == "__main__":
    main()
