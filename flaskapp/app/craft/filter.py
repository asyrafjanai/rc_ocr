
import re

IS_NO_RE = r'([a-zA-Z]\d|\d[a-zA-Z])'

def get_no_pendaftaran(text):
    text =text.upper()
    pendaftaran_re = r"(\S*)?\s?(?:NO.?O?)?\s?(?:PEN(?:D|O)AF?TA(?:B|R|F)AN:?)\s?(?:NO.?O?)?\s?(\S*\s\d*)?"
    matches = re.findall(pendaftaran_re, text, re.MULTILINE)
    is_plate_num = r'^[A-Z]+\d'

    for matched in matches:
        if re.search(is_plate_num, matched[0], re.MULTILINE):
            return matched[0].replace(' ','')
        elif re.search(is_plate_num, matched[1], re.MULTILINE):
            return matched[1].replace(' ','')
        
    return "Not Found"

def remove_noise(text):
    text = text.replace('.',' ')
    text = re.sub(r"( . )",' ',text)
    noises = ['K/BTM','M/B']
    for noise in noises:
        text=text.replace(noise,'')
    text = " ".join(text.split())
    return text

def chasis_elcl(text):
    left_chasis_re = r"(?:NO.?O?)?\s?(?:ENJIN)\s?(?:NO.?O?)?(.*)\s?(?:NO.?O?)?\s?(?:CH?ASIS:?)\s?(?:NO.?O?)?"
    matches = re.findall(left_chasis_re, text)
    for matched in matches:
        matched_text = ''.join(matched) + ' '
        matched_text = matched_text.replace(' NO ','')
        if re.search(IS_NO_RE, matched_text, re.MULTILINE):
            # matched_text = ''.join(matched_text.split()[::-1])
            return remove_noise(matched_text)
    return 'Not Found'

def chasis_ercl(text):
    ercl_re = r"(?:NO.?O?)?\s?(?:ENJIN)\s?(?:NO.?O?)?(?:\S*)\s?(?:\d*\s)?\s?(?:NO.?)?\s?(.*)?(?:NO.?O?\s?CH?ASIS:?)\s?(?:NO.?O?)?"
    matches = re.findall(ercl_re, text, re.MULTILINE)
    for matched in matches:
        matched_text = ''.join(matched)+ ' '
        if re.search(IS_NO_RE, matched_text, re.MULTILINE):
            return remove_noise(matched_text)
    return "Not Found"

def enjin_el(text):
    el_re = r"(\S*)\s?(\S*)\s?(?:NO.?O?)?\s?(?:ENJIN)\s?(?:NO?.?O?)?"
    matches = re.findall(el_re,  text)
    for matched in matches:
        if re.search(IS_NO_RE, matched[0]) and re.search('\d', matched[1]):
            return matched[0]+matched[1]
        elif re.search(IS_NO_RE, matched[1]):
            return matched[1]
    return "Not Found"

def enjin_er(text):
    er_re = r"(?:NO.?O?)?\s?(?:ENJIN)\s?(?:NO?.?O?)?\s?(\S+\s\d*)"
    matches = re.findall(er_re,  text)
    for matched in matches:
        text_matched = matched.replace(' ','')
        if re.search(IS_NO_RE, text_matched , re.MULTILINE):
            return text_matched
    return "Not Found"

def chasis_cr(text):
    cr_re = r"(?:NO.?O?)?\s?(?:CH?ASIS)\s?(?:NO?.?O?)?\s?(\S*)\s?(\S*)"
    matches = re.findall(cr_re, text)
    for matched in matches:
        if re.search(IS_NO_RE, matched[0]) and re.search(IS_NO_RE, matched[1]):
            return matched[1] + matched[0]

        if not re.search(IS_NO_RE, matched[0]) and re.search(IS_NO_RE, matched[1]):
            return matched[1]

        elif re.search(IS_NO_RE, matched[0]) and not re.search(IS_NO_RE, matched[1]):
            return matched[0]

    return "Not Found"

def is_right_enjin(text):
    ir_re = r"(?:NO.?O?)?\s?(?:ENJIN)\s?(?:NO.?O?)?\s?(\S*)"
    matches = re.findall(ir_re,  text)
    for matched in matches:
        if re.search(IS_NO_RE, matched, re.MULTILINE):
            return True
        
    return False

def is_left_enjin(text):
    il_re = r"(\S*)\s(\S*)\s?(?:NO.?O?)?\s?(?:ENJIN)\s?(?:NO.?O?)?"
    matches = re.findall(il_re,  text)
    for matched in matches:
        if re.search(IS_NO_RE, matched[0], re.MULTILINE):
            return True
        elif re.search(IS_NO_RE, matched[1], re.MULTILINE):
            return True
        
    return False

def is_right_chasis(text):
    #Check right
    exist_right = r"(?:NO.?O?)?\s?(?:CH?ASIS)\s?(?:NO.?O?)?\s?(\S*)\s?(\S*)"
    matches = re.findall(exist_right,  text)
    for matched in matches:
        if re.search(IS_NO_RE, matched[0]) or re.search(IS_NO_RE, matched[1]):
            return True
        
    return False

#New Format Regex
def get_chasis_enjin(text):
    chasis_enjin_position = "(?:NO.?O?)?\s?(?: .)*\s?(?:C\s?H\s?A\s?S\s?I?\s?S?)(?:\W)?\s?(?:NO.?O?)?\s?(?: .)*\s?(?:E\s?N\s?J\s?I?\s?N?)\s?(?: .)"
    enjin_chasis_position = "(?:(?:E|B)\s?N\s?J\s?I?\s?N?)\s?(?:IS)?(?:\W)?\s?(?:NO.?O?)?\s?(?: .)*\s?(?:C\s?H\s?A\s?S\s?I?\s?S?)(?:NO.?O?)?\s?(?:NO.?O?)?"
    regex_A = "(\S*)?\s(\S*)?\s?(?: .)*\s?(?:NO.?O?)?\s?(?: .)*\s?(?:C\s?H\s?A\s?S\s?I?\s?S?)(?:\W)?\s?(?:NO.?O?)?\s?(?: .)*\s?(?:E\s?N\s?J\s?I?\s?N?)\s?(?: .)*\s(\S*)?\s(\S*)?"
    regex_B = "(\S*)?\s(\S*)?\s?(?: .)*\s?(?:(?:E|B)\s?N\s?J\s?I?\s?N?)\s?(?:IS)?(?:\W)?\s?(?:NO.?O?)?\s?(?: .)*\s?(?:C\s?H\s?A\s?S\s?I?\s?S?)(?:NO.?O?)?\s?(?:NO.?O?)?\s?(?: .)*\s?(?: .)*\s(\S*)?\s(\S*)?"
    chasis_enjin = {}
    chasis_enjin["no_chasis"] = "Not Found"
    chasis_enjin["no_enjin"] = "Not Found"

    if re.search(chasis_enjin_position, text):
        result = re.findall(regex_A, text)
        len_result_0 = len(result[0][0])
        len_result_1 = len(result[0][1])
        len_result_2 = len(result[0][2])
        len_result_3 = len(result[0][3])
        
        if (len_result_1 > len_result_0) and (len_result_1 > len_result_2) and (len_result_1 > len_result_3):
            chasis_enjin["no_chasis"] = result[0][1]
            chasis_enjin["no_enjin"] = result[0][0]

        elif (len_result_2 > len_result_0) and (len_result_2 > len_result_1) and (len_result_2 > len_result_3):
            chasis_enjin["no_chasis"] = result[0][2]
            chasis_enjin["no_enjin"] = result[0][3]

    elif re.search(enjin_chasis_position, text):
        result = re.findall(regex_B, text)
        len_result_0 = len(result[0][0])
        len_result_1 = len(result[0][1])
        len_result_2 = len(result[0][2])
        len_result_3 = len(result[0][3])
        
        if (len_result_1 > len_result_0) and (len_result_1 > len_result_2) and (len_result_1 > len_result_3):
            chasis_enjin["no_chasis"] = result[0][1]
            chasis_enjin["no_enjin"] = result[0][0]

        elif (len_result_2 > len_result_0) and (len_result_2 > len_result_1) and (len_result_2 > len_result_3):
            chasis_enjin["no_chasis"] = result[0][2]
            chasis_enjin["no_enjin"] = result[0][3]
            
    return chasis_enjin

def is_old_format(text):
    _text = text.replace(' ','')
    keywords = ['MUATAN','WARNA','DUDUK']
    for keyword in keywords:
        if keyword in _text:
            return True
    return False
    
def get_reg_info(text):
    text = remove_noise(text.upper())
    text = text.replace('PENDAFTARAN NO PENDAFTARAN', 'PENDAFTARAN')

    no_pendaftaran = get_no_pendaftaran(text)
    no_enjin = "Not Found-"
    no_chasis = "Not Found-"

    if is_old_format(text):
        format_found = "old"
        if is_left_enjin(text):
            print('Enjin Left')
            no_enjin = enjin_el(text)
            if is_right_chasis(text):
                print('Chasis Right')
                no_chasis = chasis_cr(text)
            else:
                print('Chasis Left')
                no_chasis = chasis_elcl(text)
        elif is_right_enjin(text):
            print('Enjin Right')
            no_enjin = enjin_er(text)
            if is_right_chasis(text):
                print('Chasis Right')
                no_chasis = chasis_cr(text)
            else:
                print('Chasis Left')
                #chasis between enjin need split
                no_chasis = chasis_ercl(text)
        elif is_right_chasis(text):
            print('Chasis Right')
            no_chasis = chasis_cr(text)
    else:
        new_format = get_chasis_enjin(text)
        no_enjin = new_format['no_enjin'] 
        no_chasis = new_format['no_chasis']
        format_found = "new"
    
    return {
        "no_pendaftaran":no_pendaftaran,
        "no_enjin":no_enjin,
        "no_chasis":no_chasis
    }

def sort_prediction(textboxes, image):
    height = image.shape[0]
    y_gap = 50
    predictions = textboxes.copy()
    container = []
    for pixel in range(y_gap, height, y_gap):
        temp_predictions = []
        for prediction in predictions:
            y1 = min(prediction[1][:,1])
            y2 = max(prediction[1][:,1])
            mid_y = ((y1+ y2) /2)
            if pixel-y_gap <= mid_y < pixel:
                temp_predictions.append(prediction)
        pred_len = len(temp_predictions)
        iteration = pred_len - 1
        for i in range(0, pred_len):
            for j in range(0, iteration-i):
                x1 = min(temp_predictions[j][1][:,0])
                x2 = max(temp_predictions[j][1][:,0])
                mid_x = ((x1+ x2)/2)

                next_x1 = min(temp_predictions[j+1][1][:,0])
                next_x2 = max(temp_predictions[j+1][1][:,0])
                next_mid_x = ((next_x1+next_x2) / 2 )
                if mid_x > next_mid_x:
                    temp = temp_predictions[j]
                    temp_predictions[j] = temp_predictions[j+1]
                    temp_predictions[j+1] = temp
            
        container = container + temp_predictions
    return container

def get_textbox(text, predictions):
    for prediction in predictions:
        pred_text = prediction[0]
        if text.upper() == pred_text.upper():
            return {
                'x1':min(prediction[1][:,0]),
                'y1':min(prediction[1][:,1]),
                'x2':max(prediction[1][:,0]),
                'y2':max(prediction[1][:,1])
            }
    return 'Not found'
def get_rc_info_textbox(reg_info, predictions):
    textboxes = {}
    for k,v in reg_info.items():
        textboxes[k] = get_textbox(v, predictions)
    return textboxes
    
def filter_corrections(corrections):
    filtered_corrections = []
    for correction in corrections:
        (filename, img, prediction, submission) = correction
        for key,text in prediction['text'].items():
            if text != 'Not Found':
                coord = prediction['boxes'][key]
                textbox = img[coord['y1']:coord['y2'],
                              coord['x1']:coord['x2']].copy()
                filtered_corrections.append((textbox, None, submission[key]))
    return filtered_corrections
