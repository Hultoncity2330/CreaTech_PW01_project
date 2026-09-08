/* global Vue, APP_CONFIG, articleApi */

// Vue runs directly in the browser. Edit this file, save it, then refresh.
const { computed, createApp, ref } = Vue

createApp({
  /**
   * Prepares the state and functions used by index.html.
   */
  setup() {
    // ---------------------------------------------------------------------
    // APPLICATION STATE
    // ref() stores a reactive value. computed() derives a value from state.
    // ---------------------------------------------------------------------
    const features = APP_CONFIG.features
    const page = ref('list')
    const articles = ref([])
    const currentArticle = ref(null)
    const loading = ref(false)
    const saving = ref(false)
    const error = ref('')
    const submitError = ref('')
    const draft = ref('')
    const newArticle = ref({ name: '', content: '' })

    const otherArticles = computed(() =>
      articles.value.filter(
        (article) => article.articleUrl !== currentArticle.value?.articleUrl,
      ),
    )

    // ---------------------------------------------------------------------
    // HELPERS
    // Small, reusable functions with no network or interface side effects.
    // ---------------------------------------------------------------------
    /**
     * Converts a name to a Wikipedia-style article URL.
     * Example: "My article" becomes "My_article".
     */
    function getArticleUrl(articleName) {
      return articleName.trim().replace(/\s+/g, '_')
    }

    /**
     * Builds the frontend link used to open an article.
     */
    function getArticleLink(articleUrl) {
      return `#/article/${encodeURIComponent(articleUrl)}`
    }

    /**
     * Builds the frontend link used to edit an article.
     */
    function getEditLink(articleUrl) {
      return `${getArticleLink(articleUrl)}/edit`
    }

    /**
     * Converts an unknown JavaScript error to a readable message.
     */
    function getErrorMessage(cause) {
      console.error('[Application]', cause)
      return cause instanceof Error ? cause.message : 'Unknown error'
    }

    // ---------------------------------------------------------------------
    // DATA LOADING
    // These functions check the minimum data required by the interface.
    // ---------------------------------------------------------------------
    /**
     * Fetches and stores the article list.
     */
    async function loadArticles() {
      const data = await articleApi.list()

      const isArticleList =
        Array.isArray(data) &&
        data.every(
          (article) =>
            typeof article.name === 'string' && typeof article.articleUrl === 'string',
        )

      if (!isArticleList) {
        throw new Error('GET /list must return an array of { name, articleUrl }.')
      }

      articles.value = data
    }

    /**
     * Fetches and stores one article.
     */
    async function loadArticle(articleUrl) {
      const data = await articleApi.get(articleUrl)

      if (
        !data ||
        typeof data.name !== 'string' ||
        typeof data.articleUrl !== 'string' ||
        typeof data.content !== 'string'
      ) {
        throw new Error('The article response must contain name, articleUrl, and content.')
      }

      currentArticle.value = data
    }

    /**
     * Refreshes the article list and manages the page-level loading state.
     */
    async function refreshArticles() {
      loading.value = true
      error.value = ''

      try {
        await loadArticles()
      } catch (cause) {
        error.value = getErrorMessage(cause)
      } finally {
        loading.value = false
      }
    }

    // ---------------------------------------------------------------------
    // FORM ACTIONS
    // POST requests are kept separate from page loading.
    // ---------------------------------------------------------------------
    /**
     * Creates an article and redirects using the POST response.
     */
    async function createArticle() {
      saving.value = true
      submitError.value = ''

      try {
        const createdArticle = await articleApi.create(newArticle.value)

        if (
          typeof createdArticle?.articleUrl !== 'string' ||
          createdArticle.articleUrl.trim() === ''
        ) {
          throw new Error('POST /create must return the created article with an articleUrl.')
        }

        // Refresh before redirecting so the sidebar contains the new article.
        // If this refresh fails, the article was still created successfully.
        try {
          await loadArticles()
        } catch (cause) {
          articles.value = []
          console.warn(
            '[API] The article was created, but the list could not be refreshed.',
            cause,
          )
        }

        newArticle.value = { name: '', content: '' }
        window.location.hash = getArticleLink(createdArticle.articleUrl)
      } catch (cause) {
        submitError.value = getErrorMessage(cause)
      } finally {
        saving.value = false
      }
    }

    /**
     * Saves the edited Markdown and returns to the article page.
     */
    async function saveArticle() {
      saving.value = true
      submitError.value = ''

      try {
        const articleUrl = getArticleUrl(currentArticle.value.name)
        await articleApi.update(articleUrl, draft.value)

        window.location.hash = getArticleLink(articleUrl)
      } catch (cause) {
        submitError.value = getErrorMessage(cause)
      } finally {
        saving.value = false
      }
    }

    // ---------------------------------------------------------------------
    // ROUTING
    // The part after # selects the page. Example: #/article/My_article
    // ---------------------------------------------------------------------
    /**
     * Selects the current page from the URL and loads the required data.
     */
    async function loadCurrentPage() {
      loading.value = true
      error.value = ''
      submitError.value = ''
      currentArticle.value = null

      try {
        const path = window.location.hash.slice(1) || '/'
        const parts = path.split('/').filter(Boolean)

        if (parts[0] === 'article' && parts[1]) {
          const articleUrl = decodeURIComponent(parts[1])
          const wantsEdit = parts[2] === 'edit'

          page.value = wantsEdit && features.edit ? 'edit' : 'article'
          await loadArticle(articleUrl)

          // Direct links start without a list. Creation already refreshed it.
          if (articles.value.length === 0) {
            await loadArticles()
          }

          if (page.value === 'edit') {
            if (typeof currentArticle.value.source !== 'string') {
              throw new Error('Editing requires the article response to contain source.')
            }

            draft.value = currentArticle.value.source
          }
        } else if (parts[0] === 'create' && features.create) {
          page.value = 'create'
        } else {
          page.value = 'list'
          await loadArticles()
        }
      } catch (cause) {
        error.value = getErrorMessage(cause)
      } finally {
        loading.value = false
      }
    }

    // This root application lives as long as the page, so one listener is enough.
    window.addEventListener('hashchange', loadCurrentPage)
    loadCurrentPage()

    // Returned values and functions are available in index.html.
    return {
      features,
      page,
      articles,
      otherArticles,
      currentArticle,
      loading,
      saving,
      error,
      submitError,
      draft,
      newArticle,
      getArticleUrl,
      getArticleLink,
      getEditLink,
      refreshArticles,
      createArticle,
      saveArticle,
      loadCurrentPage,
    }
  },
}).mount('#app')
