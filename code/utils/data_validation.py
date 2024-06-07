from langchain_core.pydantic_v1 import BaseModel, Field


class SlideContentJSON(BaseModel):
    slide_number: int = Field(description="The number of the slide in the presentation")
    title: str = Field(description="Title content of the slide")
    description: str = Field(description="Body content represented as a paragraph anywhere around 5 to 30 words long")
    enumeration: list = Field(description="A list of all enumerations in the slide where each element of the list is itself a list of points which are strings")
    url: str = Field(description="URL link to a website based on the rest of the content of the slide")


class PPTContentJSON(BaseModel):
    presentation_ID : int = Field(description="Unique ID for each presentation provided in the prompt")
    subject : str = Field("The subject name provided by the user")
    topic : str = Field(description="The topic name provided by the user")
    slides: list[SlideContentJSON] = Field(description="A list of slide objects")
