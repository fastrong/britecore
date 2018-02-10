<template>
  <div v-if="loading">
    Loading...
  </div>
  <div v-else-if="!loading">
    <div class='frow'>
      <span class='rlabel'>Risk type</span>
      <el-select v-on:change="riskUpdate" class='xfield' v-model="riskType" filterable placeholder='Select risk type'>
        <el-option v-for="risk in risks" :key="risk.id" :value="risk.id" :label="risk.name"></el-option>
      </el-select>
    </div>
    <hr></hr>
    <form v-if='!loading2'>
      <div v-if="fields.date" v-for="field in fields.date" class='frow'>
        <span class='rlabel'>{{field.name}}</span>
        <el-date-picker
          v-model="datax[field.id]"
          type="date"
          placeholder="Pick a day"
          class="xfield" >
        </el-date-picker>
      </div>
      <div v-if="fields.enum" v-for="field in fields.enum" class='frow'>
        <span class='rlabel'>{{field.name}}</span>
        <el-select v-model="datax[field.id]" class='xfield' filterable placeholder='Select risk type'>
          <el-option v-for="el in field.enum" :key="el.id" :value="el.id" :label="el.name"></el-option>
        </el-select>
      </div>
      <div v-if="fields.text" v-for="field in fields.text" class='frow'>
        <span class='rlabel'>{{field.name}}</span>
        <el-input v-model="datax[field.id]" class='xfield' placeholder=''></el-input>
      </div>
      <div v-if="fields.number" v-for="field in fields.number" class='frow'>
        <span class='rlabel'>{{field.name}}</span>
        <el-input-number v-model="datax[field.id]" class='xfield' placeholder=''></el-input-number>
      </div>
    </form>
    <div v-else-if="loading2">Loading risk form...</div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Home',
  data () {
    return {
      loading : true,
      loading2 : false,
      risks : [],
      api : "https://cem2piex5l.execute-api.eu-west-1.amazonaws.com/dev",
      riskType : null,
      fields : {},
      datax : {}
    }
  },
  created(){
    axios.get(this.api + "/riskTypes").then(response => {
      console.log(response.data)
      console.log(this)
      this.risks = response.data.risks
      this.loading = false
    }).catch(e => {
      alert(e)
    })
  },
  methods:{
    riskUpdate : function(id){
      this.loading2 = true
      var newdata = {}
      axios.get(this.api + "/riskType/" + id).then(response => {
        console.log(response)
        for( var x in response.data.fields ){
          var field = response.data.fields[x]
          var type = field.type
          newdata[type] = typeof newdata[type] === 'undefined' ? [field] : newdata[type].concat(field)
        }
        this.fields = newdata
        this.loading2 = false
      }).catch(e => {
        alert(e)
      })
    }
  }
}
</script>

<style scoped>
  .xfield{
    display:inline-block;
    width:300px;
  }
  .rlabel{
    display:inline-block;
    width:150px;
    text-align:right;
    padding-right:20px;
  }
  hr{
    border-color:rgba(0,0,0,0.2);
  }
  .frow{
    padding:5px 0px;
  }
</style>
