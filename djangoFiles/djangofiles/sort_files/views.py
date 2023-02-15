import os
import shutil
from django.shortcuts import render

# Create your views here.
def sort_files(request):
    if request.method == 'POST':
        folder_path = request.POST.get('folder_path')
        sort_option = request.POST.get('sort_option')

        if sort_option == 'by_size':
            size_option = request.POST.get('size_option')
            if size_option == '<2mb':
                chunk_size = 2*1024*1024
            else:
                chunk_size = 20*1024*1024

            # Get a list of files in the folder
            file_list = os.listdir(folder_path)
            file_list.sort(key=lambda x: os.path.getsize(os.path.join(folder_path, x)))
            folder_name = 1
            folder_size = 0

            for file_name in file_list:
                file_path = os.path.join(folder_path, file_name)
                file_size = os.path.getsize(file_path)

                if folder_size + file_size > chunk_size:
                    folder_name += 1
                    folder_size = 0

                folder_output_path = os.path.join(folder_path, 'Sorted_by_size', f'Folder_{folder_name}')
                if not os.path.exists(folder_output_path):
                    os.makedirs(folder_output_path)

                output_file_path = os.path.join(folder_output_path, file_name)
                shutil.copyfile(file_path, output_file_path)

                folder_size += file_size

            return render(request, 'index.html')

        elif sort_option == 'by_number':
            file_number = request.POST.get('file_number')
            file_number = int(file_number)

            # Get a list of files in the folder
            file_list = os.listdir(folder_path)
            folder_name = 1
            file_count = 0

            for file_name in file_list:
                file_path = os.path.join(folder_path, file_name)

                if not os.path.isfile(file_path):
                    continue

                if file_count % file_number == 0:
                    folder_output_path = os.path.join(folder_path, 'Sorted_by_number', f'Folder_{folder_name}')
                    if not os.path.exists(folder_output_path):
                        os.makedirs(folder_output_path)

                    folder_name += 1

                output_file_path = os.path.join(folder_output_path, file_name)
                shutil.copyfile(file_path, output_file_path)

                file_count += 1

            return render(request, 'index.html')

    return render(request, 'index.html')