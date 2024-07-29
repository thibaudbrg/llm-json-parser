import json
import os

from colorama import Fore, Style
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from utils import print_heading, print_info, print_error, setup_logging
from dotenv import load_dotenv

# Setup custom logging
logger = setup_logging()

load_dotenv()

# Define a class for the desired JSON structure
class Review(BaseModel):
    reviewer: str
    comment: str
    date: str

class Amenity(BaseModel):
    type: str
    details: Dict[str, Any] = None

class PackageDetails(BaseModel):
    duration: str
    includes: List[Any]

class PackageContact(BaseModel):
    phone: str
    email: str
    address: Dict[str, str]

class Package(BaseModel):
    package_name: str
    price: float
    currency: str
    details: PackageDetails
    contact: PackageContact = None

class Feedback(BaseModel):
    comment: str
    details: Dict[str, Any] = None

class FormattedJSON(BaseModel):
    hotel_name: str = Field(description="Name of the hotel.")
    location: str = Field(description="Location of the hotel.")
    rating: float = Field(description="Rating of the hotel.")
    reviews: List[Review] = Field(description="List of reviews.")
    amenities: List[Amenity] = Field(description="List of amenities.")
    packages: List[Package] = Field(description="List of packages.")
    customer_feedback: List[Feedback] = Field(description="List of customer feedback.")
    additional_info: str = Field(description="Information that could not be parsed.")

def analyze_file_prompt() -> str:
    prompt = """
    Analyze the following JSON and reformat it according to the specified schema:
    - hotel_name: string
    - location: string
    - rating: float
    - reviews: list of objects with fields:
      - reviewer: string
      - comment: string
      - date: string
    - amenities: list of objects with fields:
      - type: string
      - details: optional dictionary
    - packages: list of objects with fields:
      - package_name: string
      - price: float
      - currency: string
      - details: object with fields:
        - duration: string
        - includes: list of any
      - contact: optional object with fields:
        - phone: string
        - email: string
        - address: dictionary with fields:
          - street: string
          - city: string
          - zip: string
    - customer_feedback: list of objects with fields:
      - comment: string
      - details: optional dictionary
    - additional_info: string

    If some information does not fit the schema, include it in the additional_info field.

    JSON:
    {old_json}
    """
    return prompt

def main():
    input_file_path = "llm_json_parser/inputs/bad_json.json"
    output_file_path = "llm_json_parser/outputs/good_json.json"

    if not os.path.isfile(input_file_path):
        print_error("File not found.")
        logger.error("File not found: %s", input_file_path)
        return

    with open(input_file_path, 'r') as file:
        old_json = file.read()

    prompt = ChatPromptTemplate.from_template(analyze_file_prompt())
    model = ChatOpenAI(temperature=0, model="gpt-4", streaming=True)
    parser = PydanticOutputParser(pydantic_object=FormattedJSON)

    chain =  prompt | model | parser

    new_json = chain.invoke({"old_json": old_json})
    pretty_json = json.dumps(new_json.dict(), indent=2)

    # Print and save the formatted JSON
    print_heading("Formatted JSON")
    print(Fore.BLUE + Style.BRIGHT + pretty_json + Style.RESET_ALL)

    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, 'w') as file:
        file.write(pretty_json)

    logger.info("Script finished successfully")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_error(f"An error occurred: {str(e)}")
        logger.exception("An error occurred")
