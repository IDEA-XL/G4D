from tqdm import tqdm
import os
import argparse
import pandas as pd
from prompt_tools import accuracy,get_openai_response, finish, score


def delete_column_if_exists(df, column_name):
    # Check if the column exists in the DataFrame
    if column_name in df.columns:
        # Drop the column
        df = df.drop(columns=[column_name])
    return df



def moderate(chat, model, tokenizer):
    input_ids = tokenizer.apply_chat_template(chat, return_tensors="pt")
    output = model.generate(input_ids=input_ids, max_new_tokens=3000, pad_token_id=0)
    prompt_len = input_ids.shape[-1]
    return tokenizer.decode(output[0][prompt_len:], skip_special_tokens=True)


def main(args):

    # Define result path and ensure directories exist
        results = []
        result_path = os.path.join("result", "eval", args.dataset, args.model_name)
        os.makedirs(result_path, exist_ok=True)

        # Define the full path for the result file
        result_file = os.path.join(result_path, f"{args.mode}.csv")

        # Define inference path and ensure directories exist
        inference_path = os.path.join("result", "inference", args.dataset, args.model_name)

        # Define the full path for the inference file
        inference_file = os.path.join(inference_path, f"{args.mode}.csv")

        file = pd.read_csv(inference_file)
        print(file.head())
        file = delete_column_if_exists(file, "result")
        file.insert(len(file.columns), "result", value=0)
        if args.dataset == "CB-RedTeam":
            question = list(file["jailbreak query"])
            user_answer = list(file["response"])
        elif args.dataset == "MT-bench":
            question = list(file["goal"])
            user_answer = list(file["response"])

        elif args.dataset == "CB-Benign":
            question = list(file["jailbreak input"])
            user_answer = list(file["response"])

        elif args.dataset == "MMLU-pro":
            question = list(file["question"])
            user_answer = list(file["response"])
            options = list(file["options"])
            correct_answer = list(file["answer"])
        else:
            question = []
            user_answer = []
            options = []
            correct_answer = []

        for i in tqdm(range(len(file))):
           if args.dataset == "CB-RedTeam":
                prompt = finish(question[i],  user_answer[i])
           elif args.dataset == "CB-Benign" or args.dataset == "MT-bench":
                prompt = score(question[i], user_answer[i])
           elif args.dataset == "MMLU-pro":
                prompt = accuracy(question,options, correct_answer, user_answer)
           output =  get_openai_response(prompt,model_name='gpt-4o-mini')
           print(output)
           results.append(output)
           if args.debug:
               break
        if not args.debug:
           file["result"] = results
        file.to_csv(result_file, index=False)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, default='CB-RedTeam')
    parser.add_argument('--mode', type=str, default="G4D")
    parser.add_argument('--model_name', type=str, default='gpt-4o-mini')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    main(args)