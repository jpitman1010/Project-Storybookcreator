// "user strict";
const Router = ReactRouterDOM.BrowserRouter;
const Route = ReactRouterDOM.Route;
const Link = ReactRouterDOM.Link;
const Prompt = ReactRouterDOM.Prompt
const Switch = ReactRouterDOM.Switch;
const Redirect = ReactRouterDOM.Redirect;

function Homepage() {
    return <div>Welcome to the Storybook Creator!!<br/>
                Page 1, please type 1-3 sentences into this box to start.
                <input type="textarea"></input>
            </div>
}

// <!--
// function BookPage() {
//     1. single page
//     2. cover page - creating the book
//     3. multi page storybook
//     4. upload pictures to cloudinary
//     5. user creation
//     6. User login
//     7. User library
//     book - id, 
// }


function PageTextItem(props){
    return (props.text)
}


function PageText(props) {
    const pageText = [<PageTextItem text="testing out the first sentence"></PageTextItem>]
    
    React.useEffect(() => {
        fetch('/api/pageText')
    })

    return (
        <div>
            {pageText}
        </div>
    )}
    


function App() {
    return(
        <Router>
            <div>
                <Link to="/">Page</Link>
                <Switch>
                    to something else
                    <Route path = "/">
                        <Page/>
                    </Route>
                </Switch>
            </div>
        </Router>
    )
}




ReactDOM.render(<App />, document.getElementById('root'));
