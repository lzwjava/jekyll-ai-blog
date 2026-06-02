---
audio: false
generated: false
image: false
lang: en
layout: post
title: Using Laravel
translated: false
type: post
---

If you’re diving into web development and want a framework that’s powerful yet easy to pick up, Laravel is your go-to. It’s a PHP framework that’s taken the developer world by storm, thanks to its elegant syntax, robust features, and a community that’s got your back. In this blog, I’ll walk you through the basics of getting started with Laravel and show you why it’s worth your time.

#### Step 1: Set Up Your Environment
Before you can start building with Laravel, you need the right tools. Here’s what you’ll need:
- **PHP**: Version 8.1 or higher (Laravel evolves fast, so stay updated!).
- **Composer**: This is a dependency manager for PHP. Download it from [getcomposer.org](https://getcomposer.org/).
- **A Local Server**: Something like XAMPP, WAMP, or Laravel’s built-in server works great.
- **A Terminal**: You’ll be running commands, so get comfy with your command line.

Once you’ve got these, open your terminal and install Laravel globally by running:
```
composer global require laravel/installer
```
This lets you create new Laravel projects with a single command.

#### Step 2: Create Your First Laravel Project
Ready to build something? In your terminal, navigate to the folder where you want your project to live (e.g., `cd /path/to/your/folder`), and type:
```
laravel new my-first-app
```
After a few minutes, Composer will set up a fresh Laravel project called `my-first-app`. Navigate into it:
```
cd my-first-app
```
To see it in action, start Laravel’s built-in server:
```
php artisan serve
```
Open your browser and go to `http://localhost:8000`. Boom—you’ve got a welcome page! That’s Laravel saying hello.

#### Step 3: Understand the Basics
Laravel follows an MVC (Model-View-Controller) structure, which keeps your code clean and organized:
- **Models**: Handle your data (think database tables).
- **Views**: The front-end stuff users see (HTML, CSS, etc.).
- **Controllers**: The glue that connects Models and Views.

You’ll find these in the `app/` folder. For example, controllers live in `app/Http/Controllers`, and views are in `resources/views`.

#### Step 4: Build a Simple Page
Let’s create a quick “Hello, World” page. Open `routes/web.php`—this is where you define your app’s URLs. Add this line:
```php
Route::get('/hello', function () {
    return view('hello');
});
```
Now, create a file called `hello.blade.php` in `resources/views`. Add this:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Hello, Laravel</title>
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>
```
Restart your server (or keep it running), then visit `http://localhost:8000/hello`. You’ll see your “Hello, World!” page. The `.blade.php` extension means you’re using Laravel’s Blade templating engine—super handy for dynamic content.

#### Step 5: Play with the Database
Laravel makes database work a breeze with its Eloquent ORM (Object-Relational Mapping). First, set up your database in the `.env` file (e.g., MySQL, SQLite):
```
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=your_database_name
DB_USERNAME=your_username
DB_PASSWORD=your_password
```
Create a migration to set up a table. Run:
```
php artisan make:migration create_posts_table
```
In the new file under `database/migrations`, define your table:
```php
public function up()
{
    Schema::create('posts', function (Blueprint $table) {
        $table->id();
        $table->string('title');
        $table->text('body');
        $table->timestamps();
    });
}
```
Run the migration:
```
php artisan migrate
```
Now you’ve got a `posts` table! You can create a `Post` model with:
```
php artisan make:model Post
```
This ties your table to a model you can use in your code.

#### Step 6: Keep Exploring
Laravel’s got a ton more to offer—authentication, middleware, routing, and packages via Composer. Want user login? Run:
```
php artisan make:auth
```
Need a front-end boost? Use Laravel Breeze or Jetstream. The [official docs](https://laravel.com/docs) are your best friend here.

#### Why Use Laravel?
It’s fast, secure, and saves you from reinventing the wheel. Whether you’re building a blog, an e-commerce site, or an API, Laravel’s tools—like artisan commands, Blade templates, and Eloquent—make life easier.

So, what are you waiting for? Start small, experiment, and soon you’ll be crafting web apps like a seasoned pro. Happy coding!
