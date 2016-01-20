var FaceMatch = React.createClass({
  getInitialState: function() {
    return { confidence: -1, subject: "Unknown" };
  },
  updateChar: function(data) {
    console.log(data);
    this.setState({confidence: data.p_confidence, subject: data.subject});
  },
  render: function() {
    return (
      <div className="faceMatch">
        <h1>Star Wars Facematch API</h1>
        <GithubForm onUpdateChar={this.updateChar}/>
        <div>Character Match: {this.state.subject}
          <br />
             Confidence: {this.state.confidence}
        </div>
      </div>
    );
  }
});

var GithubForm = React.createClass({
  getInitialState: function() {
    return {githubid: '', previewUrl: '#', preview: true, button: 'Find Image'};
  },
  updatePreviewURL: function() {
    $.ajax({
      url: ("https://api.github.com/users/"+this.state.githubid),
      dataType: 'json',
      success: function(data) {
        this.setState({previewUrl: data.avatar_url, preview:false, button: 'Compare'});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(status, err.toString());
      }.bind(this)
    });
  },
  handeGithubIdChange: function(e) {
    this.setState({githubid: e.target.value,
                   preview: true, button: 'Find Image'});
    this.props.onUpdateChar({});
  },
  handleSubmit: function(e) {
    e.preventDefault();
    if(this.state.preview)
    {
      this.updatePreviewURL();
      return;
    }
    $.ajax({
      url: 'https://tii3iwnhrb.execute-api.us-west-2.amazonaws.com/prod/starwarsmatch',
      data: {"imgUrl": this.state.previewUrl},
      dataType: 'json',
      success: function(data) {
        console.log(data);
        this.props.onUpdateChar(data);
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(status, err.toString());
      }.bind(this)
    });
  },
  render: function() {
    return (
      <div>
      <h2>From Github Profile</h2>
      <form className="inputForm" onSubmit={this.handleSubmit}>
        <input
          type="text"
          placeholder="Github userid"
          value={this.state.githubid}
          onChange={this.handeGithubIdChange}
        />
        <input type="submit" value={this.state.button} />
      </form>
      <img src={this.state.previewUrl}></img>
      </div>
    );
  }
});

ReactDOM.render(
  <FaceMatch/>,
  document.getElementById('content')
);
