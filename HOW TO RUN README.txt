Basic Positive Input Images are located in "input_images/pos_*.jpg"
Basic Negative Input Images are located in "input_images/pos_*.jpg"
Template Image is located in current directory as "template.jpg"

Bonus Positive 1 Input Images are located in "input_images/task3_bonus/t1_*.jpg"
Template Image for Bonus Positive 1 is located in "input_images/task3_bonus/t1.jpg"

Bonus Positive 2 Input Images are located in "input_images/task3_bonus/t2_*.jpg"
Template Image for Bonus Positive 2 is located in "input_images/task3_bonus/t2.jpg"

Bonus Positive 3 Input Images are located in "input_images/task3_bonus/t3_*.jpg"
Template Image for Bonus Positive 3 is located in "input_images/task3_bonus/t3.jpg"

Bonus Negative Input Images are located in "input_images/task3_bonus/neg_*.jpg"

The Output images are generated inside the "output_images" folder
"output_images" folder has sub folders, each for the above set of inputs

Run task3.py file in the current directory and check "output_images" folder the output

To change input add the following lines inside the "imageSets" dict of the code in line 51,

"input_set_name":{
            "path": "path_to_images/image_name.jpg",
            "template": "path_to_template_image.png"
        }


