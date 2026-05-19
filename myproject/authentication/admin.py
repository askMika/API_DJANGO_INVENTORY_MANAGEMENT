from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, TeacherProfile, LearnerProfile, CookProfile, LibrarianProfile


#  Inlines 
class TeacherProfileInline(admin.StackedInline):
    model   = TeacherProfile
    can_delete = False
    verbose_name = "Teacher Profile"


class LearnerProfileInline(admin.StackedInline):
    model   = LearnerProfile
    can_delete = False
    verbose_name = "Learner Profile"


class CookProfileInline(admin.StackedInline):
    model   = CookProfile
    can_delete = False
    verbose_name = "Cook Profile"


class LibrarianProfileInline(admin.StackedInline):
    model   = LibrarianProfile
    can_delete = False
    verbose_name = "Librarian Profile"


#  Proxy models (separate roles in admin) 
class TeacherProxy(User):
    class Meta:
        proxy               = True
        verbose_name        = "Teacher"
        verbose_name_plural = "Teachers"

class LearnerProxy(User):
    class Meta:
        proxy               = True
        verbose_name        = "Learner"
        verbose_name_plural = "Learners"

class CookProxy(User):
    class Meta:
        proxy               = True
        verbose_name        = "Cook"
        verbose_name_plural = "Cooks"

class LibrarianProxy(User):
    class Meta:
        proxy               = True
        verbose_name        = "Librarian"
        verbose_name_plural = "Librarians"


#  Main User Admin 
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display  = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active']
    list_filter   = ['role', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']

    fieldsets = UserAdmin.fieldsets + (
        ("Role", {"fields": ("role",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Role", {"fields": ("role",)}),
    )


#  Teacher Admin 
@admin.register(TeacherProxy)
class TeacherAdmin(UserAdmin):
    inlines       = [TeacherProfileInline]
    list_display  = ['username', 'email', 'first_name', 'last_name', 'is_active']
    search_fields = ['username', 'email']

    fieldsets = (
        ("Account",     {"fields": ("username", "password")}),
        ("Personal",    {"fields": ("first_name", "last_name", "email")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "first_name", "last_name", "password1", "password2")
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(role='teacher')

    def save_model(self, request, obj, form, change):
        obj.role = 'teacher'
        super().save_model(request, obj, form, change)


# Learner Admin 
@admin.register(LearnerProxy)
class LearnerAdmin(UserAdmin):
    inlines       = [LearnerProfileInline]
    list_display  = ['username', 'email', 'first_name', 'last_name', 'is_active']
    search_fields = ['username', 'email']

    fieldsets = (
        ("Account",     {"fields": ("username", "password")}),
        ("Personal",    {"fields": ("first_name", "last_name", "email")}),
        ("Permissions", {"fields": ("is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "first_name", "last_name", "password1", "password2")
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(role='learner')

    def save_model(self, request, obj, form, change):
        obj.role = 'learner'
        super().save_model(request, obj, form, change)


#  Cook Admin 
@admin.register(CookProxy)
class CookAdmin(UserAdmin):
    inlines       = [CookProfileInline]
    list_display  = ['username', 'email', 'first_name', 'last_name', 'is_active']
    search_fields = ['username', 'email']

    fieldsets = (
        ("Account",     {"fields": ("username", "password")}),
        ("Personal",    {"fields": ("first_name", "last_name", "email")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "first_name", "last_name", "password1", "password2")
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(role='cook')

    def save_model(self, request, obj, form, change):
        obj.role = 'cook'
        super().save_model(request, obj, form, change)


#  Librarian Admin 
@admin.register(LibrarianProxy)
class LibrarianAdmin(UserAdmin):
    inlines       = [LibrarianProfileInline]
    list_display  = ['username', 'email', 'first_name', 'last_name', 'is_active']
    search_fields = ['username', 'email']

    fieldsets = (
        ("Account",     {"fields": ("username", "password")}),
        ("Personal",    {"fields": ("first_name", "last_name", "email")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "first_name", "last_name", "password1", "password2")
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(role='librarian')

    def save_model(self, request, obj, form, change):
        obj.role = 'librarian'
        super().save_model(request, obj, form, change)