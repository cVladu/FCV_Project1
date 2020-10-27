# Augmentation system for CV ML algorithms
## Configuration file format
The configuration format must be **YAML**.   
The **YAML** file must have the following form, 
where terms between < and > need to be filled in by the user.
The other terms must remain as they are 

        Transformations: *Mandatory. Below this items, all the desired transformations are described.*
            <Transformation_name>: *This name will be used in image output naming* 
                func: <func_name> *The augmentation / transformation that should be applied. A list of supported augmentations can be found below*
                params: * Each function accepts a series of parameters that will be defined below * 
                    <param1_name>: <param1_value>
                    <param2_name>: <param2_value>
                    ...
                en: {True|False}  *Specify if this function shall be applied. Default True. This does not prevent the function to be applied in chain transformation *  
        Chain_Transformation: *Mandatory. Specify the chain of transformation *
            [<Transformation_name1>, <Transformation_name2>, ... ]  * A list of transformation defined in Transformations section that should be applied. The transformations will be applied in a chain, from left to right. *

## Supported transformations and parameters
The following augmentation / transformation algorithms are supported.  
_Alias will contain a list of all supported strings that map to the 
corresponding algorithm._   
_The strings are not case sensitive._
### Tint
Apply a tint on the image  
**alias:** [tint_image, tint]  
**params:**  
* value
  - **Mandatory** 
  - Percentage of tint to apply to the image. If value is higher than 1, it will be divided by 100.
  - **Type:** int or float
  - Accepted range: [0, 100].
* channel
  - **Optional**
  - The channel color with which the image shall be tinted.
  - **Type:** string
  - Accepted values: {blue, green, red}. Not case sensitive.
* mask
  - **Optional**
  - The mask represented as a list of 3 values in BGR/u8 format.
  - **Type:** list of integers
  - Accepted values: A list of 3 elements between 0 and 255. 
   
***Either mask or channel must be provided.***
### Histogram
Calculate a histogram of the image  
**alias:** [hist, histogram]  
**params:**  
* img_type
    - **Mandatory**
    - Specify the expected format of the image
    - **Type:** string
    - Accepted values: {'bgr', 'gray'}. Not case sensitive
### Brightness increase  
Increase the brightness of the image  
**alias:** [brightness, bright, modify_brightness, increase_brightness]  
**params:**
* beta
    - **Mandatory**
    - Specify the increase in every pixel value.
    - **Type:** float
    - Accepted range: [0, inf]. Even if a higher value can 
    be provided, the new pixel value will be saturated to the 
    max value of the input image format, 
    resulting in a white image.
### Contrast modification
Modify the contrast following the formula: 
`g(i, j) = alpha * f(i, j)`,  
where g(i, j) represents the new pixel value, at location (i, j)  
and f(i, j) represents the initial value at the same pixel position.    
**alias**: [contrast, modify_contrast, increase_contrast]  
**params:**
* alpha
    - **Mandatory**
    - Specify the alpha value
    - **Type:** float
    - Accepted range: [0, inf]. Undefined behavior for very large values of alpha.
### Point processing
Apply the following formula: 
`g(i, j) = alpha * f(i, j) + beta`,  
where g(i, j) represents the new pixel value, at location (i, j)  
and f(i, j) represents the initial value at the same pixel position.  
**alias:** [point_process, linear, point]  
**params:** 
* alpha:
    - **Optional.** Default value: 1.0
    - Specify the alpha value
    - **Type:** float
    - Accepted range: [-inf, inf]. Undefined values for negative or very large values.
* beta:
    - **Optional.** Default value: 0.0
    - Specify the beta value
    - **Type:** float
    - Accepted range: [-inf, inf]. Undefined behavior for 
    negative values. For very lage values, 
    the result image will be saturated to the maximum value, 
    dependent on the input image type.
### Gamma correction
Apply a gamma correct to the image.  
**alias:** [gamma, gamma_correction]  
**params:**
* gamma:
    - **Mandatory**
    - Specify the gamma in the following formula: g(x) = [f(x)]^<sup>(1/gamma)</sup>
    - **Type:** float
    - Accepted range: [0, inf]. Value must be higher than 0. Undefined behavior for very large values.
### Look up table
Apply a transformation based on the given look up table. 
The image will be transformed in a image with pixel values 
in range [0, 255]  
**alias:** [lut, lookup, lookup_table]  
**params:**
* lut:
    - **Optional**
    - Specify the look-up table for all the image channels
    - **Type:** list of integers
    - Accepted: a list with exactly 256 elements. Elements higher than 255 will be saturated. Floating points values will be converted. Undefined behavior for negative values
* blue:
    - **Optional**
    - Specify the look-up table for the blue channel
    - **Type:** list of integers
    - Accepted: a list with exactly 256 elements. Elements higher than 255 will be saturated. Floating points values will be converted. Undefined behavior for negative values
* green
    - **Optional**
    - Specify the look-up table for the green channel
    - **Type:** list of integers
    - Accepted: a list with exactly 256 elements. Elements higher than 255 will be saturated. Floating points values will be converted. Undefined behavior for negative values
* red:
    - **Optional**
    - Specify the look-up table for the red channel
    - **Type:** list of integers
    - Accepted: a list with exactly 256 elements. Elements higher than 255 will be saturated. Floating points values will be converted. Undefined behavior for negative values  
    
***Either lut or all blue green red parameters must be provided.***
### Histogram equalization
Apply histogram equalization on the image  
**alias:** [equalize_hist, eq_hist, hist_eq, hist_equalization]  
**params:**
* convert_to_gray:
    - **Optional.** Default True
    - Specify if the input image should be converted to grayscale image
    - **Type:** boolean
    - Accepted values: {True, False}
* apply_to_rgb:
    - **Optional.** Default False
    - Specify if the histogram equalization should be applied on each individual channel
    - **Type:** boolean
    - Accepted values: {True, False}  

If _convert_to_gray_ is True, the input image is converted to grayscale and
the histogram equalization is applied to the grayscale image and the result is saved,
regardless of _apply_to_rgb_ value.  
If _apply_to_rgb_ is set to False, the histogram equalization will be applied on luminance channel,
by transforming the input image to yuv format first.   
### Dilation
Apply a Dilation morphological operation.  
**alias:** [dilate, dilation]  
**params:**
* iterations:
    - **Mandatory**
    - Specify the number of iterations the dilation shall be applied for
    - **Type:** integer
    - Accepted range: [-inf, inf]. For values lower than or equal to 0, 1 iteration will be done
* kernel:
    - **Optional**
    - Specify the kernel that shall be used. The kernel must have shape (*x*, *x*), with *x* being a positive integer
    - **Type:** list of lists of {0, 1}
    - Accepted range for values: [-inf, inf]. Values should be either 0 or 1. Undefined behavior for other values. Float point numbers will be converted to integer.
* kernel_type:
    - **Optional**
    - Specify the kernel type that shall be used. The following kernel types are supported:
        - Rectangular. Aliases: [rect, rectangle, morph_rect, morph rect]. **Not** case sensitive.
        - Ellipse. Aliases: [ellipse, ell, el, morph_ellipse, morph ellipse]. **Not** case sensitive.
        - Cross. Aliases: [cross, +, morph_cross, morph cross]. **Not** case sensitive.
    - **Type:** string
    - Accepted values: Any of the above aliases.
* kernel_size:
    - **Optional**
    - Specify what shall be the size of the generated kernel, selected by _kernel_type_
    - **Type:** tuple in the form (x, x)
    - Accepted values for x: [1, inf]
* transform_binary:
    - **Optional.** Default False
    - Specify if the image should be converted to binary image first. The binary threshold is set to 127 and maximum value to 255. If False, the operation will be applied to each channel separately.
    - **Type:** boolean
    - Accepted values: {True, False}  

***Either kernel or both kernel_type and kernel_size should be provided.***     
### Erosion
Apply a Erosion morphological operation.  
**alias:** [erosion, erode]  
**params:**
* iterations:
    - **Mandatory**
    - Specify the number of iterations the dilation shall be applied for
    - **Type:** integer
    - Accepted range: [-inf, inf]. For values lower than or equal to 0, 1 iteration will be done
* kernel:
    - **Optional**
    - Specify the kernel that shall be used. The kernel must have shape (*x*, *x*), with *x* being a positive integer
    - **Type:** list of lists of {0, 1}
    - Accepted range for values: [-inf, inf]. Values should be either 0 or 1. Undefined behavior for other values. Float point numbers will be converted to integer.
* kernel_type:
    - **Optional**
    - Specify the kernel type that shall be used. The following kernel types are supported:
        - Rectangular. Aliases: [rect, rectangle, morph_rect, morph rect]. **Not** case sensitive.
        - Ellipse. Aliases: [ellipse, ell, el, morph_ellipse, morph ellipse]. **Not** case sensitive.
        - Cross. Aliases: [cross, +, morph_cross, morph cross]. **Not** case sensitive.
    - **Type:** string
    - Accepted values: Any of the above aliases.
* kernel_size:
    - **Optional**
    - Specify what shall be the size of the generated kernel, selected by _kernel_type_
    - **Type:** tuple in the form (x, x)
    - Accepted values for x: [1, inf]
* transform_binary:
    - **Optional.** Default False
    - Specify if the image should be converted to binary image first. The binary threshold is set to 127 and maximum value to 255. If False, the operation will be applied to each channel separately.
    - **Type:** boolean
    - Accepted values: {True, False}  

***Either kernel or both kernel_type and kernel_size should be provided.***
### Opening
Apply a Opening morphological operation.  
**alias:** [open, opening]  
**params:**
* iterations:
    - **Mandatory**
    - Specify the number of iterations the dilation shall be applied for
    - **Type:** integer
    - Accepted range: [-inf, inf]. For values lower than or equal to 0, 1 iteration will be done
* kernel:
    - **Optional**
    - Specify the kernel that shall be used. The kernel must have shape (*x*, *x*), with *x* being a positive integer
    - **Type:** list of lists of {0, 1}
    - Accepted range for values: [-inf, inf]. Values should be either 0 or 1. Undefined behavior for other values. Float point numbers will be converted to integer.
* kernel_type:
    - **Optional**
    - Specify the kernel type that shall be used. The following kernel types are supported:
        - Rectangular. Aliases: [rect, rectangle, morph_rect, morph rect]. **Not** case sensitive.
        - Ellipse. Aliases: [ellipse, ell, el, morph_ellipse, morph ellipse]. **Not** case sensitive.
        - Cross. Aliases: [cross, +, morph_cross, morph cross]. **Not** case sensitive.
    - **Type:** string
    - Accepted values: Any of the above aliases.
* kernel_size:
    - **Optional**
    - Specify what shall be the size of the generated kernel, selected by _kernel_type_
    - **Type:** tuple in the form (x, x)
    - Accepted values for x: [1, inf]
* transform_binary:
    - **Optional.** Default False
    - Specify if the image should be converted to binary image first. The binary threshold is set to 127 and maximum value to 255. If False, the operation will be applied to each channel separately.
    - **Type:** boolean
    - Accepted values: {True, False}  

***Either kernel or both kernel_type and kernel_size should be provided.***
### Closing
Apply a Closing morphological operation.  
**alias:** [closing, close]  
**params:**
* iterations:
    - **Mandatory**
    - Specify the number of iterations the dilation shall be applied for
    - **Type:** integer
    - Accepted range: [-inf, inf]. For values lower than or equal to 0, 1 iteration will be done
* kernel:
    - **Optional**
    - Specify the kernel that shall be used. The kernel must have shape (*x*, *x*), with *x* being a positive integer
    - **Type:** list of lists of {0, 1}
    - Accepted range for values: [-inf, inf]. Values should be either 0 or 1. Undefined behavior for other values. Float point numbers will be converted to integer.
* kernel_type:
    - **Optional**
    - Specify the kernel type that shall be used. The following kernel types are supported:
        - Rectangular. Aliases: [rect, rectangle, morph_rect, morph rect]. **Not** case sensitive.
        - Ellipse. Aliases: [ellipse, ell, el, morph_ellipse, morph ellipse]. **Not** case sensitive.
        - Cross. Aliases: [cross, +, morph_cross, morph cross]. **Not** case sensitive.
    - **Type:** string
    - Accepted values: Any of the above aliases.
* kernel_size:
    - **Optional**
    - Specify what shall be the size of the generated kernel, selected by _kernel_type_
    - **Type:** tuple in the form (x, x)
    - Accepted values for x: [1, inf]
* transform_binary:
    - **Optional.** Default False
    - Specify if the image should be converted to binary image first. The binary threshold is set to 127 and maximum value to 255. If False, the operation will be applied to each channel separately.
    - **Type:** boolean
    - Accepted values: {True, False}  

***Either kernel or both kernel_type and kernel_size should be provided.***
### Translation
Perform a translation affine transformation on the image. The resulting image will have the same dimensions as the original, with a black background.  
**alias:** [translate, translation]  
**params:**
* x_pixels:
    - **Mandatory**
    - Specify the number of pixels to translate on the x coordinate. If between -1 and 1, it will be considered as a percentage of the corresponding image size. Negative values represent a translation to left direction.
    - **Type:** float
    - Accepted range: [-inf, inf].
* y_pixels:
    - **Mandatory**
    - Specify the number of pixels to translate on the y coordinate. If between -1 and 1, it will be considered as a percentage of the corresponding image size. Negative values represent a translation to upwards direction.
    - **Type:** float
    - Accepted range: [-inf, inf].
### Scaling
Perform a scaling affine transformation on the image. The output image will have the dimensions updated to match the scaled values.  
**alias:**[scale, scaling]  
**params:**
* x_factor:
    - **Mandatory**
    - Specify the scale factor on the x axis.
    - **Type:** float
    - Accepted range: [0, inf]. Greater than 0
* y_factor:
    - **Mandatory**
    - Specify the scale factor on the y axis.
    - **Type:** float
    - Accepted range: [0, inf]. Greater than 0
### Rotation
Apply a rotation affine transformation. The rotation anchor will be the center of the image.  
**alias:** [rotate_image, rotate]
**params:**
* angle:
    - **Mandatory**
    - Specify the angle of the rotation, in degrees. Negative values specify a clockwise rotation of the image
    - **Type:** float
    - Accepted range: [-inf, inf]