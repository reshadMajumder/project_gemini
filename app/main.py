#AIzaSyBAWWY19LC79bnDwqom6xRoMteF-hExJrI
import flet as ft
import google.generativeai as genai

# Configure the Generative AI SDK
genai.configure(api_key='AIzaSyBAWWY19LC79bnDwqom6xRoMteF-hExJrI')

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    safety_settings=safety_settings,
    generation_config=generation_config,
)

def get_response(prompt):
    try:
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(prompt)
        return response.text
    except Exception as e:
        return str(e)

def main(page: ft.Page):
    page.title = "Gemini AI Chat App"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = "auto"

    prompt_text = ft.TextField(
        label="Enter your prompt here",
        multiline=True,
        width=page.width - 150,
        min_lines=3,
        border_color=ft.colors.BLUE,
        border_radius=10,
        filled=True,
        color=ft.colors.WHITE,
    )

    response_container = ft.Column(
        width=page.width - 40,
        auto_scroll=True,
        scroll="auto"
    )

    def on_submit(e):
        user_input = prompt_text.value
        if user_input:
            response_container.controls.append(
                ft.Text(f"You: {user_input}", color=ft.colors.WHITE)
            )
            response_container.controls.append(
                ft.Text("Thinking...", color=ft.colors.WHITE)
            )
            page.update()

            response = get_response(user_input)
            response_container.controls.pop()  # Remove "Thinking..." message
            response_container.controls.append(
                ft.Text(f"AI: {response}", color=ft.colors.GREEN)
            )
            page.update()

    submit_button = ft.ElevatedButton(
        text="Submit",
        on_click=on_submit,
        width=100,
        height=40,
        bgcolor=ft.colors.BLUE,
        color=ft.colors.WHITE,
    )

    input_container = ft.Row(
        controls=[
            prompt_text,
            
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(
        ft.Column(
            [
                response_container,
                ft.Divider(height=10, color="transparent"),
                input_container,
                submit_button
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )

ft.app(target=main)
