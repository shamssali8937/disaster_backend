# import uuid

# class DBService:

#     def upload_file(self, file_bytes, filename, content_type):
#         # 🔥 Simplified (replace with Firebase later)
#         return f"https://fake-storage.com/{filename}"

#     def create_report(self, user_id, media_url, disaster, severity):
#         # 🔥 Fake DB
#         return str(uuid.uuid4())


# db_service = DBService()

class DBService:

    def upload_file(self, file_bytes, filename, content_type):
        return "No Storage Used"

    def create_report(self, user_id, media_url, disaster, severity):
        return "report_123"


db_service = DBService()