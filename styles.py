"""
    Css classes to use in formating email text should be created here
"""
style = """
  div{
      margin: 30px
  }

  img{
      max-height: 500px;
      max-width: 500px;
      margin: 30px
  }
  .mystyle {
    font-size: 11pt;
    font-family: Arial;
    border-collapse: collapse;
    border: 1px solid silver;
    text-align: center;
  }

  .mystyle td,
  th {
    padding: 5px;
    text-align: center;
  }

  .mystyle tr:nth-child(even) {
    text-align: center;
  }

  .mystyle tr:hover {
    background: silver;
    cursor: pointer;
    
  }
  .danger{
    color: red
  }

  .danger-back{
    background-color: #ff6969;
  }

  .success{
    color: green;
  }

  .success-back{
    background-color: #7fd496;
  }

  .warning{
    color: yellow
  }

  .warning-back{
    background-color: #faf8a5;
  }
 
  """