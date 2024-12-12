
namespace CalibApp
{
    public partial class App : Application
    {
        public App(IServiceProvider provider)
        {
            InitializeComponent();

            //MainPage = new AppShell();
            MainPage = provider.GetService<MainPage>();
        }
    }
}
