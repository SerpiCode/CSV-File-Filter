from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

# Create your views here.

file_list = []
file_names = []

def deletar_arquivo(request, name):
    if request.method == 'GET':
        id = file_names.index(name)
        
        file_names.pop(id)
        file_list.pop(id)

        return HttpResponseRedirect(reverse('ler_csv:upload_csv'))

    return render(request, "main.html", {"file_names":file_names})

def upload_csv(request):
	
    data = {'file_names':file_names}
	
    if "GET" == request.method:
        return render(request, "main.html", data)

    error = ''

    try:
        csv_file = request.FILES["csv_file"]
        
        if not str(csv_file).endswith('.csv'):
            error = 'Error: File is not CSV type.'
            request.session['error'] = error
            
            return HttpResponseRedirect(reverse("ler_csv:upload_csv"))
        
        #if file is too large, return
        if csv_file.multiple_chunks():
            error = ("Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000)))
            request.session['error'] = error

            return HttpResponseRedirect(reverse("ler_csv:upload_csv"))
    
        file_names.append(str(csv_file))

        file_data = csv_file.read().decode("utf-8")	
    
        file_list.append(file_data)
    
    except Exception as e:
        error = "Error: " + str(e)

    request.session['error'] = error
    return HttpResponseRedirect(reverse("ler_csv:upload_csv"))


def buscar_string(request):
    string = str(request.POST['string_buscada'])

    matches = []
    found = False

    count = 0

    if len(string) > 0:
    
        for file in file_list:

            lines = file.split("\n")
            
            for line in lines:						
                if string in str(line):
                    matches.append(file_names[count])
                    
                    found = True
                    break
                    
            count += 1
                
        if not found:
            result = string + " not found."
        else:
            result = "'{s}' found in: ".format(s=string)
            for i in range(len(matches)):

                if i == 0:
                    result += str(matches[i])
                else:    
                    result = result + ', ' + str(matches[i])
            
        request.session['result'] = result

    else:
        request.session['result'] = ''
    
    return HttpResponseRedirect(reverse('ler_csv:upload_csv'))