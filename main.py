""" Gradi Interface """
import gradio as gr
from functionality.video_processing import process_live, process_video
from functionality.utils import export_video

def main():
    '''
    Gradio Interface of videos

    Parameters
    ----------
    None

    Return
    ------
    None
    '''
    title = "Object Detect Tracking and Counting"
    with gr.Blocks(theme= gr.themes.Soft()) as io:
        with gr.Tab("Video Tracking"):
            gr.Markdown(f"<center><h1>{title}</h1></center>")
            with gr.Row():
                with gr.Column():
                    input_image = gr.Video()

                with gr.Column():
                    output_image = gr.Image()

            with gr.Row():
                total_count = gr.Textbox(label = "Number of Object")

            with gr.Row():
                    input_button = gr.Button("Start Tracking")
                    input_button.click(process_video, inputs=[input_image], outputs=[output_image, total_count])
            with gr.Row():
                    input_button = gr.Button("Export Result")
                    input_button.click(export_video, inputs= None, outputs = None)

        with gr.Tab("Live Tracking") :
            gr.Markdown(f"<center><h1>{title}</h1></center>")
            with gr.Row():
                with gr.Column():
                    input_image = gr.Image(source='webcam', streaming=True)

                with gr.Column():
                    output_image = gr.Image()
            with gr.Row():
                total_count = gr.Textbox(label = "Number of Object")
            with gr.Row():
                button  = gr.Button("Start Tracking")
                button.click(process_live, inputs=[input_image], outputs=[output_image])
            with gr.Row():
                    input_button = gr.Button("Export Result")
                    input_button.click(export_video, inputs= None, outputs = None)
    io.queue()
    io.launch(debug = True)
if __name__ == "__main__":
    main()