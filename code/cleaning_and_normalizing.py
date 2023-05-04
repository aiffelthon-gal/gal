import pandas as pd
import re


def preprocess_input(df):
    df['conversation'] = df['conversation'].astype(str)

    df['conversation'] = df['conversation'].apply(lambda x: re.sub(r'(\d{1,2}):(\d{2})', r'\1시 \2분', str(x)))
    
    df['conversation'] = df['conversation'].apply(lambda x: re.sub(r'[^\w\s.?!\\]', '', x)) #슬래시 살리기 추가
    # 문자열, 공백, 온점, 물음표, 느낌표 남기고 삭제
    
    df['conversation'] = df['conversation'].apply(lambda x: re.sub('_', '', x))
    # 언더바 제거
    
    df['conversation'] = df['conversation'].apply(lambda x: re.sub(r'\.{2,}|\?{2,}|\!{2,}', lambda m: m.group(0)[0], x))
    #반복되는 특수문자 제거
    
    df['conversation'] = df['conversation'].apply(lambda x: re.sub(r'[.?!]*\?+[.?!]*', '?', x))
    # ?!.이 동시에 있을 경우 ?만 남기고 삭제
    
    df['conversation'] = df['conversation'].apply(lambda x: re.sub(r'[.!]*!', '!', x))
    #!.이 동시에 있을 경우 !만 남기고 삭제
    
    df['conversation'] = df['conversation'].apply(lambda x: re.sub(r'!1+|1+!', '!', x))
    # !11111 같은 오타를 !만 남기는 코드
    
    return df


def preprocess_single_input(txt):
    txt = txt.astype(str)

    txt = txt.re.sub(r'(\d{1,2}):(\d{2})', r'\1시 \2분')
    
    txt = txt.re.sub(r'[^\w\s.?!/]', '') 
    txt = txt.re.sub('_', '')

    txt = txt.re.sub(r'\.{2,}|\?{2,}|\!{2,}', lambda m: m.group(0)[0])
    
    txt = txt.re.sub(r'[.?!]*\?+[.?!]*', '?')
    # ?!.이 동시에 있을 경우 ?만 남기고 삭제
    txt = txt.re.sub(r'[.!]*!', '!')
    #!.이 동시에 있을 경우 !만 남기고 삭제
    txt = txt.re.sub(r'!1+|1+!', '!')
    # !11111 같은 오타를 !만 남기는 코드
    
    return txt



def preprocess_df(df):
    df['conversation'] = df['conversation'].astype(str)
    df['conversation'] = df['conversation'].apply(lambda x: re.sub(r'(\d{1,2}):(\d{2})', r'\1시 \2분', str(x)))

    df['conversation'] = df['conversation'].apply(lambda x: re.sub(r'[^\w\s.?!<oov>]', '', x))
    # 문자열, 공백, 온점, 물음표, 느낌표,<oov> 남기고 삭제
    df['conversation'] = df['conversation'].apply(lambda x: re.sub('_', '', x))
    # 언더바 제거
    
    df['conversation'] = df['conversation'].apply(lambda x: re.sub(r'\.{2,}|\?{2,}|\!{2,}', lambda m: m.group(0)[0], x))
    #반복되는 특수문자 제거
    
    df['conversation'] = df['conversation'].apply(lambda x: re.sub(r'[.?!]*\?+[.?!]*', '?', x))
    # ?!.이 동시에 있을 경우 ?만 남기고 삭제
    
    df['conversation'] = df['conversation'].apply(lambda x: re.sub(r'[.!]*!', '!', x))
    #!.이 동시에 있을 경우 !만 남기고 삭제
    
    df['conversation'] = df['conversation'].apply(lambda x: re.sub(r'!1+|1+!', '!', x))
    # !11111 같은 오타를 !만 남기는 코드
    
    return df

