import tldextract

def check_link_validity(url):
    ext = tldextract.extract(url)
    if ext.domain and ext.suffix:
        return True
    else:
        return False
    
def normalize_data(data):
    result = {}
    if data["tipe_konten"] == "link":
        result["content_type"] = "link"
        result["link"] = data["konten"]
        try:
            result["title"] = data["title"]
        except:
            result["title"] = "tanpa judul"
        try:
            result["description"] = data["description"]
        except:
            result["description"] = "tanpa description"
        
    if data["tipe_konten"] == "gambar":
        result["content_type"] = "gambar"
        result["gambar_file_id"] = data["konten"]
        try:            
            result["title"] = data["title"]
        except:
            result["title"] = "tanpa judul"
        try:
            result["description"] = data["description"]
        except:
            result["description"] = "tanpa description"
            
    if data["tipe_konten"] == "video":
        result["content_type"] = "video"
        result["video_file_id"] = data["konten"]
        try:            
            result["title"] = data["title"]
        except:
            result["title"] = "tanpa judul"
        try:
            result["description"] = data["description"]
        except:
            result["description"] = "tanpa description"
        try:            
            result["video_file_name"] = data["video_file_name"]
        except:
            result["video_file_name"] = "tanpa video_file_name"
        try:
            result["video_thumbnail"] = data["video_thumbnail"]
        except:
            result["video_thumbnail"] = "tanpa video_thumbnail"
        try:
            result["video_thumb"] = data["video_thumb"]
        except:
            result["video_thumb"] = "tanpa video_thumb"
        try:
            result["video_duration"] = data["video_duration"]
        except:
            result["video_duration"] = "tanpa video_duration"
    
    return result

import secrets
import string

def generate_token(length):
    characters = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(characters) for _ in range(length))
    return token


def get_new_info(normalization_data):
    token = []
    if normalization_data["content_type"] == "link":
        try:
            token.append(generate_token(20))
            token.append(normalization_data["link"])
        except:
            token.append(normalization_data["link"])
            token.append(normalization_data["link"])
            
    if normalization_data["content_type"] == "gambar":
        try:
            token.append(normalization_data["gambar_file_id"][0:20])
            token.append(normalization_data["gambar_file_id"])
        except:
            token.append(normalization_data["gambar_file_id"])
            token.append(normalization_data["gambar_file_id"])

    if normalization_data["content_type"] == "video":
        try:
            token.append(normalization_data["video_file_id"][0:20])
            token.append(normalization_data["video_file_id"])
        except:
            token.append(normalization_data["video_file_id"])
            token.append(normalization_data["video_file_id"])
            
    return token



            
            
        