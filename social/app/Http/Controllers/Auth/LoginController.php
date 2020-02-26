<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use App\Providers\RouteServiceProvider;
use Illuminate\Foundation\Auth\AuthenticatesUsers;
use Illuminate\Support\Facades\Log;
use App\User;
use Socialite;
class LoginController extends Controller
{
    /*
    |--------------------------------------------------------------------------
    | Login Controller
    |--------------------------------------------------------------------------
    |
    | This controller handles authenticating users for the application and
    | redirecting them to your home screen. The controller uses a trait
    | to conveniently provide its functionality to your applications.
    |
    */

    use AuthenticatesUsers;

    /**
     * Where to redirect users after login.
     *
     * @var string
     */
    protected $redirectTo = RouteServiceProvider::HOME;

    /**
     * Create a new controller instance.
     *
     * @return void
     */
    public function __construct()
    {
        $this->middleware('guest')->except('logout');
    }

    /**
  * Redirect the user to the Google authentication page.
  *
  * @return \Illuminate\Http\Response
  */ 
    
       
    public function redirectToProvider()

    {
        return Socialite::driver('google')->redirect();
      
    
        log::info('we were here');
    }
        /**
         * Obtain the user information from Google.
         *
         * @return \Illuminate\Http\Response
         */
    
     public function handleProviderCallback()
    {
        log::info('callback here -10');
        try {
            $user = Socialite::driver('google')->user();
        } catch (\Exception $e) {
            return redirect('/login');
            
        }
        log::info('callback here -9');
        // only allow people with @company.com to login
        // if (explode("@", $user->email)[1] !== 'company.com') {
        
        //     return redirect()->to('/');
            
        // }
        log::info('callback here 1');
        // check if they're an existing user
        $existingUser = User::where('email', $user->email)->first();
        log::info('callback here 2');
        if ($existingUser) {
            // log them in
           
            auth()->login($existingUser, true);
        } else {
            log::info('Something');
            // create a new user
            $newUser                  = new User;
            $newUser->name            = $user->name;
            $newUser->email           = $user->email;
            $newUser->google_id       = $user->id;
            $newUser->avatar          = $user->avatar;
            $newUser->avatar_original = $user->avatar_original;
            $newUser->save();
            auth()->login($newUser, true);
        }
        return redirect()->to('/home');
    }
}








