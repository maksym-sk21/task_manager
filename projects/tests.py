from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Project, Task
from .forms import ProjectForm, TaskForm
from django.utils import timezone
# Create your tests here.


class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.project = Project.objects.create(name="Test Project", user=self.user)

    def test_project_creation(self):
        self.assertEqual(self.project.name, "Test Project")
        self.assertEqual(self.project.user.username, "testuser")

    def test_project_string_representation(self):
        self.assertEqual(str(self.project), "Project: Test Project")


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.project = Project.objects.create(name="Test Project", user=self.user)
        self.task = Task.objects.create(name="Test Task", project=self.project, deadline=timezone.now())

    def test_task_creation(self):
        self.assertEqual(self.task.name, "Test Task")
        self.assertEqual(self.task.project.name, "Test Project")

    def test_task_priority_auto_assignment(self):
        task2 = Task.objects.create(name="Second Task", project=self.project, deadline=timezone.now())
        self.assertEqual(self.task.priority, 1)
        self.assertEqual(task2.priority, 2)

    def test_task_string_representation(self):
        self.assertEqual(str(self.task), "Task: Test Task")


class ProjectFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_valid_form(self):
        form_data = {"name": "Test Project"}
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {"name": ""}
        form = ProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class TaskFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.project = Project.objects.create(name="Test Project", user=self.user)

    def test_valid_form(self):
        form_data = {"name": "Test Task", "deadline": timezone.now()}
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {"name": "", "deadline": timezone.now()}
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class ProjectViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_project_list_view(self):
        project = Project.objects.create(name="Test Project", user=self.user)
        response = self.client.get(reverse('project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, project.name)

    def test_project_create_view(self):
        response = self.client.post(reverse('project_create'), {'name': 'New Project'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Project.objects.count(), 1)

    def test_project_update_view(self):
        project = Project.objects.create(name="Test Project", user=self.user)
        response = self.client.post(reverse('project_update', args=[project.id]), {'name': 'Updated Project'})
        project.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(project.name, "Updated Project")

    def test_project_delete_view(self):
        project = Project.objects.create(name="Test Project", user=self.user)
        response = self.client.delete(reverse('project_delete', args=[project.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Project.objects.count(), 0)


class TaskViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")
        self.project = Project.objects.create(name="Test Project", user=self.user)

    def test_task_list_view(self):
        task = Task.objects.create(name="Test Task", project=self.project, deadline=timezone.now())
        response = self.client.get(reverse('task_list', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, task.name)

    def test_task_create_view(self):
        response = self.client.post(reverse('task_create', args=[self.project.id]), {'name': 'New Task',
                                                                                     'deadline': timezone.now()})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 1)

    def test_task_update_view(self):
        task = Task.objects.create(name="Test Task", project=self.project, deadline=timezone.now())
        response = self.client.post(reverse('task_update', args=[self.project.id, task.id]),
                                    {'name': 'Updated Task',
                                     'deadline': timezone.now()
                                     })
        task.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(task.name, "Updated Task")

    def test_task_delete_view(self):
        task = Task.objects.create(name="Test Task", project=self.project, deadline=timezone.now())
        response = self.client.delete(reverse('task_delete', args=[self.project.id, task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 0)


class TaskPriorityTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")
        self.project = Project.objects.create(name="Test Project", user=self.user)

    def test_task_priority_up(self):
        task1 = Task.objects.create(name="Task 1", project=self.project, deadline=timezone.now())
        task2 = Task.objects.create(name="Task 2", project=self.project, deadline=timezone.now())
        self.client.get(reverse('task_priority_up', args=[self.project.id, task2.id]))
        task1.refresh_from_db()
        task2.refresh_from_db()
        self.assertEqual(task1.priority, 2)
        self.assertEqual(task2.priority, 1)

    def test_task_priority_down(self):
        task1 = Task.objects.create(name="Task 1", project=self.project, deadline=timezone.now())
        task2 = Task.objects.create(name="Task 2", project=self.project, deadline=timezone.now())
        self.client.get(reverse('task_priority_down', args=[self.project.id, task1.id]))
        task1.refresh_from_db()
        task2.refresh_from_db()
        self.assertEqual(task1.priority, 2)
        self.assertEqual(task2.priority, 1)

    def test_task_status_toggle(self):
        task = Task.objects.create(name="Task 1", project=self.project, deadline=timezone.now(), status=False)
        self.client.get(reverse('task_status_toggle', args=[self.project.id, task.id]))
        task.refresh_from_db()
        self.assertTrue(task.status)
