###############################################################
#Simple automation for obtaining the most frequent words from a
#youtube video or .PDF, translate them and getting a sample sentence.
#Email: jmanuel.pgp@gmail.com
#Github: https://github.com/1471juan
###############################################################
from pdfquery import PDFQuery
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from deep_translator import GoogleTranslator
import pandas as pd
import numpy as np
import string

# Load file
def file_load(directory):
    file = PDFQuery(directory)
    file.load()
    return [t.text for t in file.pq('LTTextLineHorizontal')]+[t.text for t in file.pq('LTTextBoxHorizontal')]
# Load subtitles
def subs_load(video_id, lang_id):
    return TextFormatter().format_transcript(YouTubeTranscriptApi.get_transcript(video_id, languages=[lang_id])).split()
# Load srs file
def subs_load_raw(video_id,lang_id):
    return YouTubeTranscriptApi.get_transcript(video_id, languages=[lang_id])
#Save the dataframe
def data_save(df):
    df.to_csv("./DATA.csv", encoding='utf-8', index=False)
#Clean data
def data_clean(data):
    data = data.replace('—', '')
    data=data.replace('–', '')
    data=data.replace('"', '')
    data=data.replace('”','')
    data=data.replace('“','')
    data=data.replace('?','')
    data=data.replace('‘','')
    data=data.replace('!','')
    data=data.replace('¡','')
    data=data.replace('.','')
    data=data.replace(',','')
    return data

def file_process(file,menu_option, show_frequency,show_translation,lang_id,video_id,dir):
    #create data frame
    main_data = { 'Word':  [], 'Frequency': [], 'Translation': [],'Context': [] }
    df = pd.DataFrame(main_data)

    #Clean data and sort it by frequency
    df['Word'] = [data_words.strip(string.punctuation) for data_words in str(file).split()]
    data_clean(df['Word'].str)
    df['Word']=df['Word'].replace('', np.nan)
    df['Word']=df['Word'].str.lower()

    #Get frequency values
    frequency = df['Word'].value_counts(sort=False)

    #delete duplicated values
    frequency.index.dropna()

    #delete nan values
    frequency = frequency.replace('', np.nan).dropna()

    #Set values
    data = pd.DataFrame(main_data)
    data['Word'] = frequency.index
    #Set Frequency values
    data_loop_index=0
    for i, value in frequency.items():
        data.at[data_loop_index,('Frequency')] = frequency.iloc[data_loop_index]
        data.at[data_loop_index,('Word')] = i
        data_loop_index=data_loop_index+1

    data = data.assign(Context='tmp',Translation='tmp')
    #Clean data 
    data[ data["Word"].str.contains('\\d')  ] = np.nan
    data['Word']=data['Word'].replace('', np.nan)
    data.dropna(how='any',inplace=True)
    data['Word']=data['Word'].str.lower()

    #Show translation?
    if show_translation=='n':
        data=data.drop('Translation', axis=1)
    else: 
        #get list of words to translate
        words_to_translate = data['Word'].astype(str).loc[0:].to_numpy()
        print("Translation in progress(this can take a while).")
        #translate list of words
        translated_words=GoogleTranslator(source=lang_id, target='en').translate_batch(words_to_translate.tolist())
        #Set values to column
        translation_loop_index=0
        while translation_loop_index<len(translated_words):
            data['Translation'].iat[translation_loop_index] = translated_words[translation_loop_index]
            translation_loop_index=translation_loop_index+1
        print('Translation completed.')

    #show context sentence
    if menu_option=='2':
        data_subs_list=[]
        #get data
        data_subs_raw = subs_load_raw(video_id,lang_id)
        #separate data in sentences
        for i in data_subs_raw:
            data_subs_list.append(i["text"])
        #for each word in 'data', search for a sentence and add it to the 'Context' column
        index=0
        while index<len(data['Word']):
            for item in data_subs_list:
                if data['Word'].iat[index] in item.lower():
                    data['Context'].iat[index] = item
            index=index+1
    elif menu_option=='1':
        print('Getting sentences(This can take a while)...')
        data_file_raw = file_load(dir+'.pdf')
        data_file_list = [data_words.strip(string.punctuation) for data_words in str(data_file_raw).split(sep=',')]
        #set values
        index=0
        while index<len(data['Word']):
            for item in data_file_list:
                if data['Word'].iat[index] in item.lower():
                    data['Context'].iat[index] = item
            index=index+1

    #Sort by frequency
    data = data.sort_values(by='Frequency')

    #Show frequency?
    if show_frequency=='n':
        data=data.drop('Frequency', axis=1)
    
    #Save and print data
    data_save(data)
    print("Success!")

def app():
    print('-MENU-')
    print('(1) PDF.')
    print('(2) YOUTUBE VIDEO.')
    print('(3) Exit.')
    menu_option=input("Please select an option with the number: ")
    show_frequency=input("Do you want to keep the frequencies?['y' or 'n']: ")
    show_translation=input("Do you want to keep the translations?['y' or 'n']: ")

    if menu_option=='1':
        video_id='none'
        dir = input("File name(remember to save it in the same folder as this script): ")
        lang_id = input("Language id[ example: English=en, German=de, Korean = ko, etc ]: ")
        print('Reading PDF(This can take a while)...')
        file_process(file_load(dir + ".pdf"),menu_option,show_frequency,show_translation,lang_id,video_id,dir)

    elif menu_option=='2':
        dir='none'
        video_id =input("Video id: ")
        lang_id = input("Language id[ example: English=en, German=de, Korean = ko, etc ]: ")
        file_process(subs_load(video_id,lang_id),menu_option,show_frequency,show_translation,lang_id,video_id,dir)

    elif menu_option=='3':
        pass

    else:
        print(str(menu_option)+" is not an option, try again.")
        app()

#Run app
app()

