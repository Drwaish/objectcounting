""" Utility function for processing """
import os

def text_to_srt()-> bool:
    """
    Convert Text File into .srt file for caption

    Parameters
    ----------
    None

    Return
    ------
    bool
    """
    flag = os.system("python3 text_to_subtitles.py")
    if flag == 0:
        return True
    return False

def merget_srt_to_video() -> bool:
    """
    Merge .srt file with video

    Parameters
    ----------
    None

    Return
    ------
    bool
    """
    query = "ffmpeg -i result.mp4 -vf subtitles=subtitles.srt output.mp4 -y"
    print(query)
    var = os.system(query)
    print(var)
    if var==0:
        return True
    return False

def export_video() -> None:
    """
    Download resultant video

    Parameters
    ----------
    None

    Return
    ------
    None
    """
    if text_to_srt():
        if merget_srt_to_video():
        #   files.download("output.mp4")
            print("Video Created")
