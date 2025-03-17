import os
import whisper
from openai import OpenAI
import dotenv
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage


# Load env
dotenv.load_dotenv()


# Define whisper model
def speech_to_text(audio_file_path, local_or_remote_llm):

    print("Transcribing audio file...")
    print()

    # Define local whisper model
    def local_whisper_model(audio_file_path):
        """
        https://pypi.org/project/openai-whisper/
        Size	Parameters	English-only model	Multilingual model	Required VRAM	Relative speed
        tiny	39 M	tiny.en	tiny	~1 GB	~10x
        base	74 M	base.en	base	~1 GB	~7x
        small	244 M	small.en	small	~2 GB	~4x
        medium	769 M	medium.en	medium	~5 GB	~2x
        large	1550 M	N/A	large	~10 GB	1x
        turbo	809 M	N/A	turbo	~6 GB	~8x
        """
        model = whisper.load_model("small")
        # Transcribe the audio file and return the text result
        result = model.transcribe(audio_file_path)

        return result["text"]
    
    # Define remote OpenAI Whisper model
    def remote_whisper_model(audio_file_path):

        # Pull API key from environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=api_key)

        audio_file = open(audio_file_path, "rb")
        # Create an audio transcription request using OpenAI's Whisper API
        transcribe = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            prompt="Comsource, Rey, Reymer, Aldino,"
        )
        
        return transcribe.text
    
    if local_or_remote_llm.lower() == 'l':
        return local_whisper_model(audio_file_path)
    elif local_or_remote_llm.lower() == 'r':
        return remote_whisper_model(audio_file_path)
    else:
        print("Invalid input. Defaulting to local whisper model.")
        return local_whisper_model(audio_file_path)
    

def categorise_participents(text, local_or_remote_llm):

    print(f"Categorising call participents.....")
    print()

    # Define llm
    if local_or_remote_llm.lower() == 'l':
        llm = ChatOllama(
            model="llama3.1:latest",
            temperature=0
        )
    elif local_or_remote_llm.lower() == 'r':
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
        )

    system_prompt = f"""
    Review the following conversation between a support representative and their customer. 
    Identify who is who in the conversation. 
    List the conversation in a new line for each participent and prepend with either [SUPPORT] or [CUSTOMER] followed by their [NAME] or [UNKNOWN].
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    # link llm with its system prompt
    chain = prompt | llm

    response = chain.invoke(
        [
            HumanMessage(text)
        ]
    )

    return response.content


def review_call(text, local_or_remote_llm):

    print("Reviewing call......")
    print()


    # Define llm
    if local_or_remote_llm.lower() == 'l':
        llm = ChatOllama(
            model="llama3.1:latest",
            temperature=0
        )
    elif local_or_remote_llm.lower() == 'r':
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
        )

    system_prompt = f"""
    Analyze the transcript of a support call and provide a structured evaluation:

    Caller Validated: [True/False] (Did the rep confirm at least two of: account holder name, account address, business name?)  
    Support Rep Sentiment: [Positive/Neutral/Negative]  
    Resolution or Clear Next Steps: [Yes/No]  
    Positive and Sincere Signoff: [True/False]  
    Overall Rating: [1-5] (Based on professionalism, clarity, and resolution)  

    Keep responses concise and objective.
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    # link llm with its system prompt
    chain = prompt | llm

    response = chain.invoke(
        [
            HumanMessage(text)
        ]
    )

    return response.content