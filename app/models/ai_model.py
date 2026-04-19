# import os
# import tempfile
# from gradio_client import Client, handle_file

# class AIModel:
#     def __init__(self):
#         # Initialize the client
#         self.client = Client("shamssali/disaster-ai-api")

#     async def analyze(self, image_bytes: bytes):
#         # 1. Create a temporary file path
#         # We don't use the 'with' statement here because we need to 
#         # close the file BEFORE Gradio tries to read it.
#         temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
#         temp_path = temp.name
        
#         try:
#             # 2. Write the bytes and close immediately to release the Windows lock
#             temp.write(image_bytes)
#             temp.close() 

#             # 3. Call Hugging Face Space
#             # Now that the file is closed, Gradio has permission to read it
#             result = self.client.predict(
#                 image=handle_file(temp_path),
#                 api_name="/predict"
#             )
            
#             # 4. Extract results
#             disaster = result.get("disaster", "Unknown")
#             severity = result.get("severity", 0.0)
            
#             return disaster, severity

#         except Exception as e:
#             print(f"AI Model Error: {e}")
#             return "Detection Error", 0.0
            
#         finally:
         
#             if os.path.exists(temp_path):
#                 try:
#                     os.remove(temp_path)
#                 except Exception:
#                     pass 

# # THIS LINE IS MISSING OR NAMED WRONG - ADD IT HERE:
# ai_model = AIModel()








import os
import tempfile
import httpx
from gradio_client import Client, handle_file

class AIModel:
    def __init__(self):
        # We use a longer timeout for video processing
        self.client = Client("shamssali/disaster-ai-api")

    def _guess_extension(self, data: bytes) -> str:
        # Simple magic byte check
        if data.startswith(b'\xff\xd8'): return '.jpg'
        if data.startswith(b'\x89PNG'): return '.png'
        if b'ftyp' in data[:20]: return '.mp4' # Basic video detection
        return '.png' # Default fallback

    async def analyze(self, media_bytes: bytes, filename: str = None):
        # Determine extension
        if filename and os.path.splitext(filename)[1]:
            ext = os.path.splitext(filename)[1].lower()
        else:
            ext = self._guess_extension(media_bytes)

        # Create temp file
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
        temp_path = temp.name
        
        try:
            temp.write(media_bytes)
            temp.close() 

            # FIX: Use 'file_obj' instead of 'image'
            result = self.client.predict(
                file_obj=handle_file(temp_path),
                api_name="/predict"
            )
            
            disaster = result.get("disaster", "Unknown")
            severity = result.get("severity", 0.0)
            
            return disaster, severity

        except Exception as e:
            print(f"AI Model Error: {e}")
            return "Detection Error", 0.0
            
        finally:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass 

# Initialize the instance
ai_model = AIModel()












# import os
# import tempfile
# import mimetypes
# import httpx
# from gradio_client import Client, handle_file

# class AIModel:
#     def __init__(self):
#         # Long timeout for video processing (15 minutes)
#         self.timeout = httpx.Timeout(900.0, connect=900.0)
#         self.client = Client("shamssali/disaster-ai-api")

#     def _guess_extension(self, data: bytes) -> str:
#         """Guess file extension from magic bytes (mime type)."""
#         # Images
#         if data.startswith(b'\x89PNG\r\n\x1a\n'):
#             return '.png'
#         if data.startswith(b'\xff\xd8'):          # JPEG
#             return '.jpg'
#         if data.startswith(b'RIFF') and data[8:12] == b'WEBP':
#             return '.webp'
#         # Videos
#         if data.startswith(b'\x00\x00\x00\x18ftypmp42') or data.startswith(b'\x00\x00\x00\x1cftypmp4'):
#             return '.mp4'
#         if data.startswith(b'RIFF') and data[8:12] == b'AVI ':
#             return '.avi'
#         if data.startswith(b'\x00\x00\x00\x1cftypqt  '):
#             return '.mov'
#         if data.startswith(b'\x1aE\xdf\xa3'):
#             return '.mkv'
#         # Default fallback
#         return '.bin'

#     async def analyze(self, media_bytes: bytes, filename: str = None):
#         """
#         Send media (image or video) to the Hugging Face Space.
#         :param media_bytes: raw bytes of the file
#         :param filename: original filename (recommended, for correct extension)
#         :return: (disaster_type, severity)
#         """
#         # Determine file extension
#         if filename and os.path.splitext(filename)[1]:
#             ext = os.path.splitext(filename)[1].lower()
#             # Normalize .jpeg to .jpg (optional, but keeps consistency)
#             if ext == '.jpeg':
#                 ext = '.jpg'
#         else:
#             ext = self._guess_extension(media_bytes)
#             if ext == '.bin':
#                 ext = '.png'   # final fallback

#         # Create a temporary file with the correct extension
#         temp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
#         temp_path = temp.name

#         try:
#             temp.write(media_bytes)
#             temp.close()

#             print(f"[DEBUG] Sending {filename or 'file'}{ext} to Space...")
#             result = self.client.predict(
#                 file_obj=handle_file(temp_path),
#                 api_name="/predict"
#             )
#             print(f"[DEBUG] Space response: {result}")
#             return result.get("disaster", "Unknown"), result.get("severity", 0.0)

#         except Exception as e:
#             print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#             print(f"CRASH ON SPACE: {e}")
#             print("Check Hugging Face Space Logs (Logs tab) for details.")
#             print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#             return "Server Error", 0.0

#         finally:
#             if os.path.exists(temp_path):
#                 try:
#                     os.remove(temp_path)
#                 except Exception:
#                     pass

# # Singleton instance
# ai_model = AIModel()