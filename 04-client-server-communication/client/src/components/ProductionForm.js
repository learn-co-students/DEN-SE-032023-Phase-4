import React, {useState} from 'react'
import styled from 'styled-components'
import { useHistory } from 'react-router-dom'
// Instead of using useState, we will use useFormik, a react hook to manage state, includes helper functions
//We can also handle validations on our frontend by using Yup, a schema builder, a way to view and modify objects in our app
// 6.✅ Verify formik and yup have been added to our package.json dependencies 
  // import the useFormik hook from formik
  // import * as yup for yup
  import {useFormik} from "formik"
  import * as yup from "yup"



function ProductionForm({addProduction}) {

  //set a state for errors
  const [errors, setError] = useState()

  const history = useHistory()
  // 7.✅ Use yup to create client side validations
  const formSchema = yup.object().shape({
    title: yup.string().required("Please Enter a title"),
    budget: yup.number().positive()
  })

  const formik = useFormik({
    initialValues:{
      title: "",
      budget: "",
      genre: "",
      director: "",
      description: ""
    },
    validationSchema: formSchema,
    onSubmit:(values) => {
      fetch('/productions', {
        method: "POST",
        headers: {
          "Content-Type":"application/json"
        },
        body: JSON.stringify(values)
      })
      .then(res => {
        if(res.ok){
          res.json().then(production => {
            addProduction(production)
            history.push(`/productions/${production.id}`)
          })
        }
        else{
          res.json().then(errors => setError(errors.message))
        }
      })
    }
  })


  // 9.✅ useFormik hook and create post request


    return (
      <div className='App'>
      <Form onSubmit={formik.handleSubmit}>
        {errors&& <h3 style={{color: "red"}}>{errors.toUpperCase()}</h3>}
        {/* {formik.errors&& Object.values(formik.errors).map(error => <h3 style={{color: "green"}}>{error.toUpperCase()}</h3>)} */}
        <label>Title </label>
        <input type='text' name='title' value={formik.values.title} onChange={formik.handleChange}/>
        
        <label> Genre</label>
        <input type='text' name='genre' value={formik.values.genre} onChange={formik.handleChange} />
      
        <label>Budget</label>
        <input type='number' name='budget' value={formik.values.budget} onChange={formik.handleChange}/>
      
        <label>Image</label>
        <input type='text' name='image'  value={formik.values.image} onChange={formik.handleChange}/>
      
        <label>Director</label>
        <input type='text' name='director' value={formik.values.director} onChange={formik.handleChange}/>
      
        <label>Description</label>
        <textarea type='text' rows='4' cols='50' name='description' value={formik.values.description} onChange={formik.handleChange} />
      
        <input type='submit' />
      </Form> 
      </div>
    )
  }
  
  export default ProductionForm

  const Form = styled.form`
    display:flex;
    flex-direction:column;
    width: 400px;
    margin:auto;
    font-family:Arial;
    font-size:30px;
    input[type=submit]{
      background-color:#42ddf5;
      color: white;
      height:40px;
      font-family:Arial;
      font-size:30px;
      margin-top:10px;
      margin-bottom:10px;
    }
  `