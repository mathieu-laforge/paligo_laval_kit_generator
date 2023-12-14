import os


def useTemplate(template):
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    file_name = os.path.join(file_dir, template)
    with open(file_name, "r", encoding="UTF-8") as f:
        read = str(f.read())
        return read
        
#useTemplate(cfg.paligo_sgdru_rules["validations"]["template"])