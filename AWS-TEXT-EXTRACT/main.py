import json
import boto3

client = boto3.client("textract")


def read_image():
    with open("images/lista-material-escolar.jpeg", "rb") as file:
        response = client.detect_document_text(
            Document={"Bytes": file.read()}
        )

    with open("response.json", "w") as file:
        json.dump(response, file)


def get_lines():
    try:
        with open("response.json") as file:
            data = json.load(file)
    except FileNotFoundError:
        read_image()
        return get_lines()

    return [
        block["Text"]
        for block in data["Blocks"]
        if block["BlockType"] == "LINE"
    ]


for line in get_lines():
    print(line)