<template>
  <div class='mycontainer container'>
    <input v-model='searchQuery' class='single-input mb-20' placeholder='Filter your events...'>
    <VuePerfectScrollbar class="scroll-area container" :settings="settings">
      <div class='timeline' v-if='anyArticle()'>
        <div v-for='(dateWithArticles, date) in searchedArticles' :key="dateWithArticles.id">
          <p v-if='dateWithArticles.length > 0' class='date'>{{ date }}</p>
          <div v-for='article in dateWithArticles' class='article' :key="article.id" @click="info(article.title)" style="cursor:pointer">
            <span class='dot'></span>
            <p class='article-date'>{{ article.published_at }}</p>
            <h3><a>{{ article.title }}</a></h3>
            <p>{{ article.teaser }}</p>
          </div>
        </div>
      </div>
      <p v-else>No articles found.</p>
    </VuePerfectScrollbar>
  </div>
</template>

<script>
import VuePerfectScrollbar from 'vue-perfect-scrollbar'
export default {
    name: 'Events',
    props: {
      datesArticles:Object,
    },
    data() {
      return {
        searchQuery: '',
        settings: {
          maxScrollbarLength: 60,
          suppressScrollX: true,
        }
      }
    },
    components:{VuePerfectScrollbar},
    computed: {
      searchedArticles() {
        var searchRegex = new RegExp(this.searchQuery, 'i');
        var searchedObj = {};
  
        if(this.searchQuery == '') {
           return this.datesArticles;
        }
  
        for(var date in this.datesArticles) {
          searchedObj[date] = this.datesArticles[date].filter((article) => {
            return searchRegex.test(article.title) ||
                   searchRegex.test(article.teaser) ||
                   searchRegex.test(article.published_at) ||
                   searchRegex.test(date);
          });
        }
        return searchedObj;
      }
    },
    methods: {
      myUpdate(){
        this.$forceUpdate
      },
      info(title){
          console.log(title)
      },
      anyArticle() {
        return this.countAllArticles() ? true : false;
      },
      countAllArticles() {
        var count = 0;
        for(var date in this.searchedArticles) {
          count += this.searchedArticles[date].length;
        }
        return count;
      }
    }
}


/*
Example of data to pass to component

datesArticles: {
        'September': [
          {
            title: 'Five',
            slug: 'five',
            teaser: 'five',
            published_at: '30.09.2016.'
          },
          {
            title: 'Four',
            slug: 'four',
            teaser: 'four',
            published_at: '15.09.2016.'
          }
        ],
        'April': [
          {
            title: 'Three',
            slug: 'three',
            teaser: 'three',
            published_at: '14.04.2016.'
          },
          {
            title: 'Two and a half',
            slug: 'two-and-a-half',
            teaser: 'two and a half',
            published_at: '02.04.2016.'
          }
        ],
        'December': [
          {
            title: 'Two',
            slug: 'two',
            teaser: 'two',
            published_at: '25.12.2015.'
          },
          {
            title: 'One',
            slug: 'one',
            teaser: 'one',
            published_at: '01.12.2015.'
          }
        ]
      },
*/

</script>

<style scoped>
.mycontainer {
	margin: 0 auto;
	max-width: 80%;
  margin-bottom: 20px;
}

.mycontainer .search-box {
	padding: 10px;
	margin: 20px 0;
	border: 1px solid black;
	border-radius: 5px;
}

.mycontainer .timeline {
	position: relative;
	border-left: 2px solid black;
}

.mycontainer .timeline .date {
	display: inline-block;
  font-size: 1.5rem;
	padding: 5px;
	position: relative;
  color:#616161;
  font-weight: bold;
	left: 15px;
	margin: 15px 0;
}

.mycontainer .timeline .date:before {
	content: '';
	position: absolute;
	top: 50%;
	left: -16px;
	border: 1px solid black;
	width: 14px;
}

.mycontainer .timeline .article {
	position: relative;
  max-width: 95%;
	left: 20px;
	box-shadow: 1px 5px 10px 1px rgba(0, 0, 0, 0.2);
	border-radius: 5px;
	padding: 10px;
	margin: 10px 0;
}

.mycontainer .timeline .article:hover {
	box-shadow: 0px 5px 10px 0px rgba(0, 0, 0, 0.4);
}

.mycontainer .timeline .article a {
	color: #006699;
	text-decoration: none;
}

.mycontainer .timeline .article .article-date {
	font-weight: 300;
	font-size: 14px;
}

.mycontainer .timeline .article .dot {
	display: block;
	position: absolute;
	width: 15px;
	height: 15px;
	border-radius: 50%;
	background: #006699;
	left: -27.5px;
	top: calc(50% - 5px);
}

.scroll-area {
  position: relative;
  margin: auto;
  width: 100%;
  height: 800px;
}
</style>
