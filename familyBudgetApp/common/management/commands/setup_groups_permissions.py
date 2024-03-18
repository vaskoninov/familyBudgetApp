import json
import os

from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Setup initial groups and permissions from a JSON file.'

    def handle(self, *args, **options):
        json_path = os.path.join(settings.BASE_DIR, 'familyBudgetApp/common/config/groups_permissions.json')

        with open(json_path, 'r') as file:
            groups_permissions = json.load(file)

        for group_info in groups_permissions:
            group, created = Group.objects.get_or_create(name=group_info['group'])

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created new group: {group_info["group"]}'))
                for perm_code in group_info['permissions']:
                    app_label, codename = perm_code.split('.')
                    try:
                        permission = Permission.objects.get(content_type__app_label=app_label, codename=codename)
                        group.permissions.add(permission)
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'Permission {perm_code} does not exist. Skipping.'))
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'Group "{group_info["group"]}" already exists. No changes made.'))

            self.stdout.write(self.style.SUCCESS('Group setup completed.'))