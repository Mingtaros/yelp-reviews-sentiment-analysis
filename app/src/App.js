import React from "react";
import "./App.css";

class ReviewInput extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: "",
      sentiment: "",
      error: null,
      showSentiment: false,
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  handleSubmit(event) {
    fetch("http://6dce216e6332.ngrok.io" /* insert endpoint here */, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: this.state.value }),
    })
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({
            value: this.state.value,
            sentiment: result.label,
            showSentiment: true,
          });
        },
        (error) => {
          this.setState({
            error,
            showSentiment: true,
          });
        }
      );
    event.preventDefault();
  }

  render() {
    return (
      <div>
        <div className="top-header-margin"></div>
        <form onSubmit={this.handleSubmit}>
          <h2 className="header">Enter your review here</h2>
          <label>
            <textarea
              className="review-textarea"
              rows="5"
              cols="100"
              value={this.state.value}
              onChange={this.handleChange}
              placeholder="Write a review here..."
            />
          </label>
          <br></br>
          <input
            type="submit"
            value="Predict Sentiment"
            className="submit-button"
          />
        </form>

        {this.state.showSentiment ? (
          <div>
            {this.state.error ? (
              <h1 className="sentiment">Error</h1>
            ) : (
              <h1 className="sentiment">{this.state.sentiment}</h1>
            )}
          </div>
        ) : null}
      </div>
    );
  }
}

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <div>
          <ReviewInput />
        </div>
      </header>
    </div>
  );
}

export default App;
