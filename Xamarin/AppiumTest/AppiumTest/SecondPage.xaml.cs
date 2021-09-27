using System;

namespace AppiumTest
{
    public partial class SecondPage
    {
        public SecondPage()
        {
            InitializeComponent();
        }

        private async void Button_OnClicked(object sender, EventArgs e)
        {
            await Navigation.PopAsync();
        }
    }
}