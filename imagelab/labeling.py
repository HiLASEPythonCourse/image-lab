import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from skimage.color import label2rgb
from skimage.filters import threshold_otsu
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.segmentation import clear_border


def label_image(image_data):
    image = image_data[:, :, 0]

    # apply threshold
    thresh = threshold_otsu(image)
    bw = closing(image > thresh, square(3))

    # remove artifacts connected to image border
    cleared = clear_border(bw)

    # label image regions
    return label(cleared)


def plot_labeled_image(label_image, image_data):
    fig, ax = plt.subplots(figsize=(10, 6))
    image = image_data[:, :, 0]
    # to make the background transparent, pass the value of `bg_label`,
    # and leave `bg_color` as `None` and `kind` as `overlay`
    image_label_overlay = label2rgb(label_image, image=image, bg_label=0)

    ax.imshow(image_label_overlay)

    for region in regionprops(label_image):
        # take regions with large enough areas
        if region.area >= 100:
            # draw rectangle around segmented coins
            minr, minc, maxr, maxc = region.bbox
            rect = mpatches.Rectangle(
                (minc, minr), maxc - minc, maxr - minr, fill=False, edgecolor="red", linewidth=2
            )
            ax.add_patch(rect)

    ax.set_axis_off()
    plt.tight_layout()
    return fig
