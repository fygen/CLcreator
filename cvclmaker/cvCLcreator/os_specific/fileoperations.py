import os
from django.http import HttpResponse
from django.utils.encoding import smart_str

def handle_file_download(file_path):
    """
    Handles the file download logic and returns an HTTP response.
    """
    full_file_path = os.path.join('your/file/directory/', file_path)
    
    # Ensure the file exists
    if not os.path.exists(full_file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    # Open the file and prepare the response
    with open(full_file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename="{smart_str(os.path.basename(full_file_path))}"'
        response['X-Sendfile'] = smart_str(full_file_path)
    
    return response