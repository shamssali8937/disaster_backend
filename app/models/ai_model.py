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








# import os
# import tempfile
# import httpx
# from gradio_client import Client, handle_file

# class AIModel:
#     def __init__(self):
#         # We use a longer timeout for video processing
#         self.client = Client("shamssali/disaster-ai-api")

#     def _guess_extension(self, data: bytes) -> str:
#         # Simple magic byte check
#         if data.startswith(b'\xff\xd8'): return '.jpg'
#         if data.startswith(b'\x89PNG'): return '.png'
#         if b'ftyp' in data[:20]: return '.mp4' # Basic video detection
#         return '.png' # Default fallback

#     async def analyze(self, media_bytes: bytes, filename: str = None):
#         # Determine extension
#         if filename and os.path.splitext(filename)[1]:
#             ext = os.path.splitext(filename)[1].lower()
#         else:
#             ext = self._guess_extension(media_bytes)

#         # Create temp file
#         temp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
#         temp_path = temp.name
        
#         try:
#             temp.write(media_bytes)
#             temp.close() 

#             # FIX: Use 'file_obj' instead of 'image'
#             result = self.client.predict(
#                 file_obj=handle_file(temp_path),
#                 api_name="/predict"
#             )
            
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

# # Initialize the instance
# ai_model = AIModel()











import os
import re
import tempfile
from gradio_client import Client, handle_file


class AIModel:

    def __init__(self):
        self.client = Client("shamssali/s2")

    def _guess_extension(self, data: bytes) -> str:

        if data.startswith(b'\xff\xd8'):
            return '.jpg'

        if data.startswith(b'\x89PNG'):
            return '.png'

        return '.png'

    async def analyze(
        self,
        pre_image_bytes: bytes,
        post_image_bytes: bytes,
        pre_filename: str = None,
        post_filename: str = None
    ):

        pre_ext = (
            os.path.splitext(pre_filename)[1].lower()
            if pre_filename and os.path.splitext(pre_filename)[1]
            else self._guess_extension(pre_image_bytes)
        )

        post_ext = (
            os.path.splitext(post_filename)[1].lower()
            if post_filename and os.path.splitext(post_filename)[1]
            else self._guess_extension(post_image_bytes)
        )

        pre_temp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=pre_ext
        )

        post_temp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=post_ext
        )

        pre_temp_path = pre_temp.name
        post_temp_path = post_temp.name

        try:

            # Save images

            pre_temp.write(pre_image_bytes)
            pre_temp.close()

            post_temp.write(post_image_bytes)
            post_temp.close()

            # ------------------------------------------------
            # HF API CALL
            # ------------------------------------------------

            result = self.client.predict(
                pre_image=handle_file(pre_temp_path),
                post_image=handle_file(post_temp_path),
                api_name="/predict"
            )

            print("HF RESPONSE:", result)

            # ------------------------------------------------
            # IMPORTANT FIX
            # ------------------------------------------------

            # Get ONLY first text response
            result_text = result[0]

            # ------------------------------------------------
            # DAMAGE INTENSITY
            # ------------------------------------------------

            class_match = re.search(
                r"Predicted Class\s*:\s*(.+)",
                result_text
            )

            damage_intensity = (
                class_match.group(1).strip()
                if class_match
                else "Unknown"
            )

            # Clean line breaks
            damage_intensity = damage_intensity.split("\n")[0].strip()

            # ------------------------------------------------
            # CONFIDENCE
            # ------------------------------------------------

            confidence_match = re.search(
                r"Confidence\s*:\s*([\d.]+)",
                result_text
            )

            confidence = (
                float(confidence_match.group(1))
                if confidence_match
                else 0.0
            )

            # ------------------------------------------------
            # SEVERITY
            # ------------------------------------------------

            severity_match = re.search(
                r"Severity\s*:\s*([\d.]+)",
                result_text
            )

            severity = (
                float(severity_match.group(1))
                if severity_match
                else 0.0
            )

            return {
                "damage_intensity": damage_intensity,
                "confidence": confidence,
                "severity": severity
            }

        except Exception as e:

            print("AI MODEL ERROR:", e)

            return {
                "damage_intensity": "Detection Error",
                "confidence": 0.0,
                "severity": 0.0
            }

        finally:

            if os.path.exists(pre_temp_path):
                try:
                    os.remove(pre_temp_path)
                except:
                    pass

            if os.path.exists(post_temp_path):
                try:
                    os.remove(post_temp_path)
                except:
                    pass


ai_model = AIModel()