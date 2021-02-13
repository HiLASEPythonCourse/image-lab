import skimage.io
import matplotlib.pyplot as plt
import streamlit as st
from imagelab import labeling


def read_image(input_file):
    image_data = skimage.io.imread(input_file)
    return image_data


def main():
    st.header("Input")
    input_file = st.file_uploader("Image file")
    if not input_file:
        st.warning("Load image first")
        return
    image_data = read_image(input_file)
    fig, ax = plt.subplots()
    ax.imshow(image_data)
    st.write(fig)

    st.header("Label image")
    image_labels = labeling.label_image(image_data)
    fig = labeling.plot_labeled_image(image_labels, image_data)
    st.write(fig)

if __name__ == "__main__":
    main()
