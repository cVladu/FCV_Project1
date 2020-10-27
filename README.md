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
_Func will contain a list of all supported strings that map to the 
corresponding algorithm._   
_The strings are not case sensitive._
### Tint
Apply a tint on the image  
**func:** [tint_image, tint]  
**params:**  
* value
  - **Mandatory** 
  - Percentage of tint to apply to the image. If value is higher than 1, it will be divided by 100.
  - Accepted range: [0, 100].
* channel
  - **Optional**
  - The channel color with which the image shall be tinted.
  - Accepted values: {blue, green, red}. Not case sensitive.
* mask
  - **Optional**
  - The mask represented as a list of 3 values in BGR/u8 format.
  - Accepted values: A list of 3 elements between 0 and 255. 
   
***Either mask or channel must be provided.***
### Histogram
Calculate a histogram of the image  
**func:** [hist, histogram]  
**params:**  
* img_type
    - **Mandatory**
    - Specify the expected format of the image
    - Accepted values: {'bgr', 'gray'}. Not case sensitive
### Brightness increase  
Increase the brightness of the image  
**func:** [brightness, bright, modify_brightness, increase_brightness]  
**params:**
* beta
    - **Mandatory**
    - Specify the increase in every pixel value.
    - Accepted range: [0, inf]. Even if a higher value can 
    be provided, the new pixel value will be saturated to the 
    max value of the input image format, 
    resulting in a white image.
### Contrast modification
Modify the contrast following the formula: 
`g(i, j) = alpha * f(i, j)`,  
where g(i, j) represents the new pixel value, at location (i, j)  
and f(i, j) represents the initial value at the same pixel position.    
**func**: [contrast, modify_contrast, increase_contrast]  
**params:**
* alpha
    - **Mandatory**
    - Specify the alpha value
    - Accepted range: [0, inf]. Undefined behavior for very large values of alpha.
### Point processing
Apply the following formula: 
`g(i, j) = alpha * f(i, j) + beta`,  
where g(i, j) represents the new pixel value, at location (i, j)  
and f(i, j) represents the initial value at the same pixel position.  
**func**: [point_process, linear, point]  
**params:** 
* alpha:
    - **Optional.** Default value: 1.0
    - Specify the alpha value
    - Accepted range: [-inf, inf]. Undefined values for negative or very large values.
* beta:
    - **Optional.** Default value: 0.0
    - Specify the beta value
    - Accepted range: [-inf, inf]. Undefined behavior for 
    negative values. For very lage values, 
    the result image will be saturated to the maximum value, 
    dependent on the input image type.

