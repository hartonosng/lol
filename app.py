import chainlit as cl
import asyncio

# Streaming per karakter untuk satu row table
async def stream_single_row(message: cl.Message, left_text: str, right_text: str, delay: float = 0.05):
    max_len = max(len(left_text), len(right_text))
    left_stream = ""
    right_stream = ""

    for i in range(1, max_len + 1):
        left_stream = left_text[:i] if i <= len(left_text) else left_text
        right_stream = right_text[:i] if i <= len(right_text) else right_text

        table_md = f"| Response A | Response B |\n| --- | --- |\n| {left_stream} | {right_stream} |"
        message.content = table_md
        await message.update()
        await asyncio.sleep(delay)

@cl.on_chat_start
async def start():
    await cl.Message("Halo! Demo A/B testing dengan voting icon 👍").send()

@cl.on_message
async def on_message(message: cl.Message):
    user_text = message.content or "(kosong)"
    
    response_a = f"Response A: Terima kasih atas pesan '{user_text}'. Ini contoh respons panjang untuk testing."
    response_b = f"Response B: Halo! Pesan '{user_text}' sudah kami terima. Ini contoh respons panjang untuk testing."

    # Kirim table
    ab_msg = await cl.Message(content=" ").send()
    await stream_single_row(ab_msg, response_a, response_b)

    # Tambahkan action buttons untuk voting
    actions = [
    cl.Action(
        name="vote_a",
        # icon="heart",              # Change the icon (emoji or supported icon name)
        label="❤️ I like Response A",  # Custom label text
        payload={"choice": "A"}
    ),
    cl.Action(
        name="vote_b",
        # icon="star",
        label="⭐ I like Response B",
        payload={"choice": "B"}
    )
]

    await cl.Message("Pilih respon yang kamu suka:", actions=actions).send()

# Callback untuk tombol vote A
@cl.action_callback("vote_a")
async def vote_a_callback(action: cl.Action):
    print("Payload vote A:", action.payload)
    await cl.Message("Kamu memilih 👍 Response A").send()

# Callback untuk tombol vote B
@cl.action_callback("vote_b")
async def vote_b_callback(action: cl.Action):
    print("Payload vote B:", action.payload)
    await cl.Message("Kamu memilih 👍 Response B").send()
