import logging
import requests
import zipfile
from io import BytesIO

from rdmo.domain.models import Attribute
from rdmo.projects.models.value import Value

logger = logging.getLogger(__name__)

attribute_uri_prefix = "https://dev-rdmo.int.mpdl.mpg.de/terms"
attribute_commit_uri_key_prefix = "project/metadata/publication/gitlab/commit/"

def zip(content_files):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(
        file=zip_buffer,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as zip_archive:
        for name, file_content in content_files.items():
            zip_archive.writestr(zinfo_or_arcname=name, data=file_content)

    zip_buffer.seek(0)

    return zip_buffer

def unzip(zip_buffer):
    content_files = {}
    with zipfile.ZipFile(zip_buffer) as zip:
        for name in zip.namelist():
            with zip.open(name) as file:
                content = file.read()
                content_files[name] = content

    return content_files
                

def get_project_licenses(project):
    # https://github.com/spdx/license-list-data
    attribute = Attribute.objects.get(uri='https://rdmorganiser.github.io/terms/domain/smp/software-license')
    spdx_ids = [license.value for license in project.values.filter(attribute=attribute)]
    
    license_contents = []
    for id in spdx_ids:
        url = 'https://api.github.com/repos/spdx/license-list-data/contents/text/{spdx_id}.txt'.format(spdx_id=id)        
        response = requests.get(url, headers={'Accept': 'application/vnd.github+json'})
        try:
            response.raise_for_status()
            base64_string_of_content = response.json().get('content')
            license_contents.append({
                'content': base64_string_of_content,
                'path': f'contents/LICENSE-{id}',
                'export_format': f'license-{id.lower()}'
            })
        except:
            continue
        
    return license_contents

def get_project_value_with_record_id(project, export_format):
    record_id_attribute, _created = Attribute.objects.get_or_create(uri_prefix=attribute_uri_prefix,
                                                          key=f'{attribute_commit_uri_key_prefix}{export_format}')
    
    project_commit_value = project.values.filter(attribute=record_id_attribute).first()
    return project_commit_value, record_id_attribute

def get_record_id_from_project_value(project, export_format):
    project_commit_value, _record_id_attribute = get_project_value_with_record_id(project, export_format)

    if project_commit_value is not None:
        return project_commit_value.text
    else:
        return None

def set_record_id_on_project_value(project, record_id, export_format):
    if project is None or record_id is None:
        return

    project_commit_value, record_id_attribute = get_project_value_with_record_id(project, export_format)

    if project_commit_value is None:
        # create the value with text and add it
        value = Value(project=project, attribute=record_id_attribute, text=record_id)
        value.save()
        project.values.add(value)
    elif project_commit_value.text != record_id:
        # update and overwrite the value.text
        project_commit_value.text = record_id
        project_commit_value.save()

def clear_record_id_from_project_value(project, export_format):
    """Clear the record_id text from the project's values by setting it to an empty string."""
    set_record_id_on_project_value(project, '', export_format)