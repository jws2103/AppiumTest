using Xamarin.Forms;

namespace AppiumTest
{
    public class BasePage : ContentPage
    {
        protected BasePage()
        {
            NavigationPage.SetHasNavigationBar(this, false);
        }
    }
}