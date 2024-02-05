from argparse import ArgumentParser
from openai import OpenAI
import os

COMMAND = 'COMMAND'
NO_OUTPUT = 'NO OUTPUT'


def main():
    arg_parser = ArgumentParser(prog='API Documentation Creator')
    arg_parser.add_argument('-m', '--method', required=True)
    arg_parser.add_argument('-p', '--path', required=True, nargs='+')

    args = arg_parser.parse_args()
    method = args.method
    paths = ','.join(args.path)

    client = OpenAI(api_key=os.environ['OPENAI_KEY'])

    system_message = f"""You are a software engineer assistant for writing REST API documentation. You will be provided
with java class name and method that is entrypoint for an API resource. Spring Boot MVC framework is used to create
application. You need to create documentation in a confluence format. It should include: 1) code block with http method
and API path; 2) request parameters table; 3) request body table; 4) code block with json body example; 5) response 
fields table; 6) code block with json response example. Table fields name, type, required (TRUE or FALSE), description.
Use linux commands to get all needed classes content. Use find command to search for java class files. Get file content 
using cat command. Issue commands use '{COMMAND}' word as the first line. Use only 1 command per message. Do not mix 
multiple commands or command and documentation in one message. Do not include description or explanation for commands. 
Use response data as context for the following command. Output full result as a final message only without intermediate 
results. If command output returns {NO_OUTPUT} just use class name for documentation skipping internal details. Use 
commands to get parameters and response classes content including child fields types. For types like 
Mono<Response<Model>> use commands to get Response type details also.
"""

    conversation = [
        {
            "role": "system",
            "content": system_message
        },
        {
            "role": "user",
            "content": f"Class and method: {method}. Search paths: {paths}"
        }
    ]

    while True:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=conversation,
            temperature=0.2,
            max_tokens=500,
            top_p=1
        )

        response_message = response.choices[0].message
        conversation.append(response_message)

        content = response_message.content
        if content.startswith(f"{COMMAND}\n"):
            command = content.replace(f"{COMMAND}\n", "")
            print(command)

            cmd_output = os.popen(command).read()
            if cmd_output == '':
                cmd_output = NO_OUTPUT

            message = {
                "role": "user",
                "content": cmd_output
            }
            conversation.append(message)
        else:
            print(content)
            break


if __name__ == '__main__':
    main()
