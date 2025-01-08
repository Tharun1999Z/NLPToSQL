#config.py

class Config:
    AZURE_API_KEY = "4076f9d9575544e384c754dd47ecf804"
    AZURE_API_VERSION = "2024-05-01-preview"
    AZURE_ENDPOINT = "https://newkeyss.openai.azure.com/"
    DATA_FILE = "dataset_meeting.xlsx"
    PAGE_TITLE = "Zion AI Chatbot"
    LAYOUT = "wide"

    SCHEMA = """
    CREATE TABLE ProgramData (
        ProgramCode VARCHAR(20),
        Franchise VARCHAR(50),
        ClientEventType VARCHAR(100),
        LocationType VARCHAR(50),
        MeetingTopic VARCHAR(255),
        ProgramStatus VARCHAR(50),
        Month VARCHAR(20),
        ProgramDate DATE,
        ProgramTime TIME,
        SpeakerName VARCHAR(100),
        HostName VARCHAR(100),
        Territory VARCHAR(20),
        VenueName VARCHAR(100),
        VenueCity VARCHAR(100),
        VenueState VARCHAR(50),
        VenueZip VARCHAR(20),
        SurveyNeutralme VARCHAR(255),
        Question VARCHAR(500),
        Responses TEXT,
        LASTMODIFIEDDATE DATETIME,
        SurveyTaker_Rep VARCHAR(100),
        Admin Fee DECIMAL(10, 2)
    );
    """
