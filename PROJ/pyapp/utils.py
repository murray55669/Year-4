import cv2
from PIL import Image, ImageTk


def blank_image(root):
    return ImageTk.PhotoImage(Image.new('RGBA', (640, 640), (0, 0, 0, 0)), master=root)


def thresh_image(image, thresh_val):
    blur = cv2.GaussianBlur(image, (5, 5), 0)
    blur_gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    retval, thresh_gray = cv2.threshold(blur_gray, thresh_val, 255, cv2.THRESH_BINARY_INV)
    threshed = cv2.bitwise_and(image, image, mask=thresh_gray)

    b, g, r = cv2.split(threshed)
    return cv2.merge((r, g, b, thresh_gray))


def calc_scale_ratio(desired_width, image_shape):
    return desired_width / float(image_shape[1])


def hex_to_rgba(value):
    value = value.lstrip('#')
    lv = len(value)
    rgb = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    return rgb+(255,)


def stack_images(images):
    # takes an array of images and stacks them up
    if len(images) > 0:
        stack = images[0]

        for image in images[1:]:
            stack_gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
            ret, stack_mask = cv2.threshold(stack_gray, 10, 255, cv2.THRESH_BINARY)
            stack_mask_inv = cv2.bitwise_not(stack_mask)
            stack = cv2.bitwise_and(stack, stack, mask=stack_mask_inv)
            image = cv2.bitwise_and(image, image, mask=stack_mask)

            stack = cv2.add(stack, image)

        return stack