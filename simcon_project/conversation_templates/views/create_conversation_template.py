import json
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import ensure_csrf_cookie
from conversation_templates.models import TemplateNodeChoice, TemplateNode, ConversationTemplate
from users.models import Researcher

def is_researcher(user):
    return user.is_authenticated and user.is_researcher

@user_passes_test(is_researcher)
@ensure_csrf_cookie  # guarantees csrf cookie is generated even though html does not contain {% csrf_token %}
def CreateConversationTemplateView(request):

    if(request.method == 'GET'):
        return render(request, 'template_management/create_conversation_template.html')

    elif(request.method == 'POST'):
        stored_nodes_dict = {}
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        conv_temlpate = ConversationTemplate(
            name=body['templateName'],
            description=body['templateDescription'],
            researcher=Researcher.objects.get(email=request.user.email)) #TODO Not sure if this is the best way to do it?
        conv_temlpate.save()

        # First pass to create all TemplateNode objects
        for received_node in body['nodes']:
            received_node_body = received_node[1]
            new_node = TemplateNode(
                description=received_node_body['description'],
                video_url=received_node_body['videoURL'],
                start=received_node_body['isFirst'],
                terminal=received_node_body['isTerminal'],
                parent_template=conv_temlpate)
            stored_nodes_dict[received_node[0]] = new_node
            new_node.save()

        # Go over nodes in request body again, this time creating TemplateNodeChoice objects
        for received_node in body['nodes']:
            for choice in received_node[1]['responseChoices']:
                TemplateNodeChoice(
                    choice_text=choice['description'],
                    parent_template=stored_nodes_dict.get(received_node[0]),
                    destination_node=stored_nodes_dict.get(choice['destinationIndex'])).save()

        return HttpResponse(status=250)
