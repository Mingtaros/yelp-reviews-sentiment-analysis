import React from "react";
import "./App.css";

class ReviewInput extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: "",
      sentiment: "",
      showSentiment: false,
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  handleSubmit(event) {
    this.setState({
      sentiment: "some sentiment",
      showSentiment: true,
    });
    event.preventDefault();
  }

  render() {
    return (
      <div>
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
            <h1 className='sentiment'>{this.state.sentiment}</h1>
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
