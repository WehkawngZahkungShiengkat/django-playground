from django.db import migrations

def populate_post_category(apps, schema_editor):
    Post = apps.get_model('post', 'Post')
    Category = apps.get_model('post', 'PostCategory')

    for post in Post.objects.all():
        category_str = post.category
        if category_str:
            try:
                category = Category.objects.get(name=category_str)
                post.post_category = category
                post.save()
            except Category.DoesNotExist:
                # Create a new PostCategory if it doesn't exist
                new_category = Category.objects.create(name=category_str)
                post.post_category = new_category
                post.save()

class Migration(migrations.Migration):

    dependencies = [
        ('post', '0015_alter_post_post_category'),
    ]

    operations = [
        migrations.RunPython(populate_post_category),
    ]