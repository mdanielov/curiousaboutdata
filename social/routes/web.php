<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});
Route::get('/redirect/google', 'Auth\LoginController@redirectToProvider');
Route::get('/callback', 'Auth\LoginController@handleProviderCallback');

Route::get('/redirect/facebook', 'SocialAuthFacebookController@redirect');
Route::get('/callback/facebook', 'SocialAuthFacebookController@callback');

Auth::routes();

Route::get('/home', 'HomeController@index')->name('home');





