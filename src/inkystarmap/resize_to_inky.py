from PIL import Image

def get_image_dimensions(image_name):
    """ Get image dimensions
    """
    img = Image.open(image_name)
    img_width, img_height = img.size
    return img_width, img_height


def get_image_aspect_ratio(img_width, img_height):
    """ Get image aspect ratio
    """
    aspect_ratio = img_width / img_height
    return aspect_ratio


def calculate_image_resize_plan(image_aspect_ratio, inky_aspect_ratio, 
                                inky_display_width, inky_display_height):
    """ Make image resize plan
    """
    if image_aspect_ratio < inky_aspect_ratio:
        # Resize image width to twice the inky width
        resize_width = inky_display_width
        resize_height = int(inky_display_width / image_aspect_ratio)
    elif image_aspect_ratio > inky_aspect_ratio:
        # Resize image height to twice the inky height
        resize_height = inky_display_height
        resize_width = int(inky_display_height * image_aspect_ratio)
    else:
        # Resize image height to inky height
        resize_width = inky_display_width
        resize_height = inky_display_height
    return resize_width, resize_height


def resize_and_crop_image(image_name, resize_width, resize_height, crop_width, crop_height):
    """ Resize and crop image
    """
    img = Image.open(image_name)
    img = img.resize((resize_width, resize_height))
    # img_cropped_area = (0, 0, crop_width, crop_height)


    # make the cropped area in the middle of the image sized crop_width x crop_height
    img_cropped_area = (int((resize_width - crop_width) / 2),
                        int((resize_height - crop_height) / 2),
                        int((resize_width + crop_width) / 2),
                        int((resize_height + crop_height) / 2))
    print("Cropped area:", img_cropped_area)

    img = img.crop(img_cropped_area)
    return img


def resize_to_inky(image_name, inky_display_width, inky_display_height):
    img_width, img_height = get_image_dimensions(image_name)
    print(f"Image dimensions: {img_width} x {img_height}")
    image_aspect_ratio = get_image_aspect_ratio(img_width, img_height)
    print(f"Image aspect ratio: {image_aspect_ratio}")
    inky_aspect_ratio = get_image_aspect_ratio(inky_display_width, inky_display_height)
    print(f"Inky aspect ratio: {inky_aspect_ratio}")

    resize_width, resize_height = calculate_image_resize_plan(image_aspect_ratio, 
                                                              inky_aspect_ratio, 
                                                              inky_display_width, 
                                                              inky_display_height)
    print(f"Resize plan: {resize_width} x {resize_height}")

    img = resize_and_crop_image(image_name, resize_width,
                                resize_height, inky_display_width,
                                inky_display_height)
    return img
