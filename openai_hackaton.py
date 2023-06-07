import os
import time

import config
import openai

model_engine = "davinci"
n_epochs = 3
batch_size = 4
learning_rate = 1e-5
max_tokens = 1024

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
training_file = os.path.join(__location__, 'training_data.jsonl')
validation_file = os.path.join(__location__, 'validation_data.jsonl')
openai.api_key = config.CHAT_GPT_API_KEY


def prepare_training_data():
    # Read our installation documents and prepare it to
    print("hi")
    create_args = {
        "training_file": training_file,
        "validation_file": validation_file,
        "model": "davinci",
        "n_epochs": 15,
        "batch_size": 3,
        "learning_rate_multiplier": 0.3
    }

    fine_tuning_job = openai.FineTune.create(**create_args)
    #fine-tune the model
    # fine_tuning_job = openai.FineTune.create(
    #     model_engine=model_engine,
    #     n_epochs=n_epochs,
    #     batch_size=batch_size,
    #     learning_rate=learning_rate,
    #     max_tokens=max_tokens,
    #     training_file=os.path.abspath(training_file),
    #     validation_file=os.path.abspath(validation_file),
    # )

    job_id = fine_tuning_job["id"]
    print(f"Fine-tuning job created with ID: {job_id}")

    #monitor the progress of the fine-tuning job
    while True:
        fine_tuning_status = openai.FineTune.get_status(job_id)
        status = fine_tuning_status["status"]
        print(f"Fine-tuning job status: {status}")

        if status in ["completed", "failed"]:
            break

        time.sleep(60)

    #use the fine-tuned model
    fine_tuned_model_id = fine_tuning_status["fine_tuned_model_id"]

    # Use the fine-tuned model for text generation
    def generate_text(prompt, model_id, max_tokens=50):
        response = openai.Completion.create(
            engine=model_id,
            prompt=prompt,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text.strip()

    prompt = "Your example prompt goes here."
    generated_text = generate_text(prompt, fine_tuned_model_id)
    print(f"Generated text: {generated_text}")



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


