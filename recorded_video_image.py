""" Server processing"""
from PIL import Image
from tqdm.notebook import tqdm
import supervision as sv
from functionality.model import load_model


TARGET_VIDEO_PATH = "result.mp4"
model = load_model()


def flask_video(source_video_path : str ):
    """
    In this method video processing will be done.

    Parameters
    ----------
    source_video_path
      Video to detect track and count object

    Return
    ------
    Image
      Return the process frame .
    """
    # if os.path.isdir(TARGET_VIDEO_PATH):

    #     os.system("rm -rf /content/vid_out")
    #     os.system("mkdir vid_out")
      # create BYTETracker instance
    tokenize = source_video_path.split(".")
    if tokenize[-1] not in ("mp4"):
      return "Type Error"

    byte_tracker = sv.ByteTrack()
    # create VideoInfo instance
    video_info = sv.VideoInfo.from_video_path(source_video_path)
    # create frame generator
    generator = sv.get_video_frames_generator(source_video_path)
    # create LineCounter instance
    # create instance of BoxAnnotator and LineCounterAnnotator
    box_annotator = sv.BoxAnnotator(thickness=4, text_thickness=4, text_scale=1)
    print("Video Info" , video_info)
    # open target video file
    with sv.VideoSink(TARGET_VIDEO_PATH, video_info) as sink:
        # loop over video frames
        for frame in tqdm(generator, total=video_info.total_frames):
            # model prediction on single frame and conversion to supervision Detections
            results = model(frame)
            detections = sv.Detections(
                xyxy=results[0].boxes.xyxy.cpu().numpy(),
                confidence=results[0].boxes.conf.cpu().numpy(),
                class_id=results[0].boxes.cls.cpu().numpy().astype(int)
            )
            detections = byte_tracker.update_with_detections(detections)
            labels = [
                f"#{tracker_id} {model.model.names[class_id]} {confidence:0.2f}"
                for _, _, confidence, class_id, tracker_id
                in detections
            ]
            with open("subtitles.txt","a", encoding='utf-8') as file:
              file.writelines(str(labels) + '\n' + '\n')
            frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)
            sink.write_frame(frame)
    return "0k"

def image_processing(path : str) -> None:
    """
        In this method processing will be done on image.

        Parameters
        ----------
        path
        Path of Image send by user

        Return
        ------
        None
        """
    # create instance of BoxAnnotator
    box_annotator = sv.BoxAnnotator(thickness=2, text_thickness=2, text_scale=1)
    img = Image.open(path)
    # model prediction on single frame and conversion to supervision Detections
    results = model(img)
    detections = sv.Detections(
        xyxy=results[0].boxes.xyxy.cpu().numpy(),
        confidence=results[0].boxes.conf.cpu().numpy(),
        class_id=results[0].boxes.cls.cpu().numpy().astype(int)
    )
    # format custom labels
    labels = [
        f"{model.model.names[class_id]} {confidence:0.2f}"
        for _, confidence, class_id, tracker_id
        in detections
    ]
    # annotate and display frame
    frame = box_annotator.annotate(scene= img, detections=detections, labels=labels)
    frame.save("temp.jpg")