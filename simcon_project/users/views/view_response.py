from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from users.forms import UpdateFeedback
from conversation_templates.models import TemplateResponse, TemplateNodeResponse


def ViewResponse(request, responseid="6b64f89a-176c-4b61-b9ac-29ede63e78b7"):
    response = TemplateResponse.objects.get(id=responseid)
    if response is not None:
        nodes = []
        num_nodes = TemplateNodeResponse.objects.filter(parent_template_response=response).count()
        for i in range(1, num_nodes+1):
            if TemplateNodeResponse.objects.get(parent_template_response=response, position_in_sequence=i):
                nodes.append(TemplateNodeResponse.objects.get(parent_template_response=response,
                                                              position_in_sequence=i))
            else:
                break

        return render(request, 'view_response.html', {'response_nodes': nodes, 'response': response})
    else:
        return render(request, 'invalid_response.html')


def UpdateResponseFeedback(request, pk):
    feedback_instance = get_object_or_404(TemplateResponse, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = UpdateFeedback(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            feedback_instance.feedback = form.cleaned_data['feedback']
            feedback_instance.save()

        # redirect to a new URL:
        return HttpResponseRedirect(reverse('ViewResponse'))

    # If this is a GET (or any other method) create the default form.
    else:
        default_feedback = feedback_instance.feedback
        form = UpdateFeedback(initial={'feedback': default_feedback})

    context = {
        'form': form,
        'feedback_instance': feedback_instance,
    }

    return render(request, 'view_response.html', context)
