import config
import openai


def prepare_training_data():
    # Read our installation documents and prepare it to



def main():
    prepare_training_data()
    openai.api_key = config.CHAT_GPT_API_KEY
    chatgptPrompt = '''I would like to update my current version to the latest and greatest. Can you please do it for me?'''
    print(openai.Model.list())
    id = 'text-davinci-003'

    response = openai.Completion.create(
        model=id,
        prompt=chatgptPrompt
    )

    print("RESPONSE")
    print(str(response))





if __name__ == '__main__':
    main()


